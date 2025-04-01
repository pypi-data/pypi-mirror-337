import glob
import itertools
import json
import pathlib
import subprocess
import sys
import tempfile
from collections import Counter
from itertools import product
from os import path

# Set matplotlib backend to non-interactive 'Agg' to prevent GUI session
import matplotlib
matplotlib.use('Agg')

import logomaker
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from Bio import AlignIO, SeqIO
from matplotlib.cm import ScalarMappable
from sklearn.neighbors import KernelDensity

abs_path = str(pathlib.Path(__file__).parent.resolve())


class HMMScanner:

    def get_UP_seq(self, UP_id):
        URL = "https://rest.uniprot.org/uniprotkb/{}.fasta".format(UP_id)
        response = requests.get(URL)
        with tempfile.NamedTemporaryFile() as self.temp_UP_file:
            open(self.temp_UP_file.name, "wb").write(response.content)
            return self.hmmalign_RRMs(self.temp_UP_file.name)

    def hmmssearch_RRMs(self, fasta_file, outfile):
        bashCmd = [
            "hmmsearch",
            "-A",
            outfile,
            "-E",
            "0.003",
            "--domE",
            "0.003",
            "--incE",
            "0.003",
            abs_path + "/alignment_data/rrm_bound.hmm",  # hmmdb
            "{}".format(fasta_file),  # seqfile
        ]

        process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print("command:", bashCmd, file=sys.stderr)
            print("stdout:", stdout, file=sys.stderr)
            print("stdout:", stderr, file=sys.stderr)
            exit("hmmalign failure")

        try:
            align = AlignIO.read(outfile, "stockholm")
            self.n_found_RRM = len(align)
            print("{} RRM domains have been identified".format(self.n_found_RRM))

        except ValueError:  # Error when no sequence is found below threshold
            print("None RRM has been identified in the input sequence/s")
            exit()

    def hmmalign_RRMs(self, fasta_file):
        with tempfile.NamedTemporaryFile() as self.temp_hmmsearch_file, tempfile.NamedTemporaryFile() as self.temp_hmmalign_file:
            # First identify wether there are RRMs and where they are
            self.hmmssearch_RRMs(fasta_file, self.temp_hmmsearch_file.name)

            bashCmd = [
                "hmmalign",
                "--mapali",
                abs_path + "/alignment_data/"
                "rrm_bound_domains_aligned_processed_squeezed.fasta",
                "-o",
                self.temp_hmmalign_file.name,
                abs_path + "/alignment_data/rrm_bound.hmm",
                "{}".format(self.temp_hmmsearch_file.name),
            ]

            process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                print("command:", bashCmd, file=sys.stderr)
                print("stdout:", stdout, file=sys.stderr)
                print("stdout:", stderr, file=sys.stderr)
                exit("hmmalign failure")

            align = AlignIO.read(self.temp_hmmalign_file.name, "stockholm")
            new_seq_to_map = list(str(align[0].seq).upper())
            seqs_dict = {
                aln_seq.id: str(aln_seq.seq) for aln_seq in align[-self.n_found_RRM :]
            }

            # In case new gaps are added, map back to the original positions
            if len(list(seqs_dict.values())[0]) > 243:
                # Get the new mapping manually #TODO: MUST be a better way...
                original_alignment = SeqIO.parse(
                    open(
                        abs_path
                        + "/alignment_data/rrm_bound_domains_aligned_processed_squeezed.fasta"
                    ),
                    "fasta",
                )

                orig_seq_to_map = list(
                    [str(i.seq).upper() for i in original_alignment][0]
                )

                aln_length = len(orig_seq_to_map)

                new_mapping = {}
                new_gaps = 0
                for i in range(aln_length):
                    if new_seq_to_map[: i + 1] == orig_seq_to_map[: i + 1]:
                        new_mapping[i] = i + new_gaps
                    else:
                        while new_seq_to_map[: i + 1] != orig_seq_to_map[: i + 1]:
                            new_gaps += 1
                            new_seq_to_map.pop(i)
                        new_mapping[i] = i + new_gaps

                # Update the seqs_dict to keep the right size and relevant part
                # IT IS NOT THE REAL SEQUENCE
                for seqid, seq in seqs_dict.items():
                    updated_seq = "".join(
                        [seq[new_mapping[pos]] for pos in new_mapping.keys()]
                    )
                    seqs_dict[seqid] = updated_seq

            return seqs_dict


class RNAScoring:
    def __init__(self):
        self.scores_dict = {}

        # Protein bias
        self.fasta_rna_aln = path.join(
            abs_path, "alignment_data/RNAs_aligned_cluster_0_nt_full_refined.fasta"
        )
        self.fasta_prot_aln = path.join(
            abs_path,
            "alignment_data/rrm_bound_domains_aligned_processed_squeezed.fasta",
        )
        # Input data
        self.master_aln = path.join(
            abs_path,
            "alignment_data/RRM_master_interaction_info_with_nt_unbiased_cluster_0.json",
        )

        self.rna_aln = path.join(
            abs_path, "alignment_data/neighbours_rna_cluster_0.json"
        )


    @property
    def rna_seqs(self):
        return list(SeqIO.parse(open(self.fasta_rna_aln), "fasta"))

    @property
    def rna_seqs_dict_full(self):
        return {i.id: str(i.seq) for i in self.rna_seqs}

    @property
    def bias_dict(self):
        return Counter(
            [i.id.split("_")[0] + "_" + i.id.split("_")[1] for i in self.rna_seqs]
        )

    @property
    def prot_seqs(self):
        return list(SeqIO.parse(open(self.fasta_prot_aln), "fasta"))

    @property
    def prot_seqs_dict_full(self):
        return {"_".join(i.id.split("_")[:2]): str(i.seq) for i in self.prot_seqs}

    @property
    def aln_data(self):
        return json.load(open(self.master_aln))

    @property
    def rna_data(self):
        return json.load(open(self.rna_aln))

    @property
    def entries_list(self):
        return list(self.rna_seqs_dict_full.keys())

    def load_scores(
        self,
        scores_folder=path.join(abs_path, "alignment_data/precalculated_scores/*.pkl"),
    ):
        self.all_df_dict = {}

        for file in glob.glob(scores_folder):
            df = pd.read_pickle(file)
            res_num = int(file.split("/")[-1].split(".")[0].split("_")[0])
            nuc_num = int(file.split("/")[-1].split(".")[0].split("_")[1])

            self.all_df_dict[(res_num, nuc_num)] = df

        return self.all_df_dict

    def score_out_seq(self, rrm_seq, rna_seq, rna_pos_range):
        window_size = rna_pos_range[1] - rna_pos_range[0]

        self.scores_dict = {}
        for i in range(len(rna_seq) - (window_size - 1)):
            rna_window = rna_seq[i : i + window_size]
            self.scores_dict[rna_window] = []
            scores_by_pos = []

            for selected_pos, df in self.load_scores().items():
                if rna_pos_range[0] <= selected_pos[1] < rna_pos_range[1]:
                    nuc = rna_window[selected_pos[1] - rna_pos_range[0]]
                    res = rrm_seq[selected_pos[0]].upper()
                    if res != "-" and nuc != "-":
                        scores_by_pos.append(df.loc[res][nuc])

            self.scores_dict[rna_window] = np.nanmean(scores_by_pos)

        return self.scores_dict

    def plot_rna_kde_to_file(self, rna_seq, window_size, plot_path, dpi=300, x_min=-0.4, x_max=0.8, title=None, wrap_title=False):
        self.plot_rna_kde(
            rna_seq=rna_seq, scores_dict=self.scores_dict, window_size=window_size,
            x_min=x_min, x_max=x_max, title=title, wrap_title=wrap_title
        )
        plt.savefig(plot_path, dpi=dpi)

    def plot_rna_kde(self, rna_seq, scores_dict, window_size, x_min=-0.4, x_max=0.8, title=None, wrap_title=False):
        with open(
            path.join(
                abs_path, "alignment_data/leave-one-out_positive_scores_avg_perc_20.txt"
            ),
            "r",
        ) as pos_file:
            pos_scores = [float(i.strip()) for i in pos_file.readlines()]

        with open(
            path.join(
                abs_path, "alignment_data/leave-one-out_negative_scores_avg_perc_20.txt"
            ),
            "r",
        ) as neg_file:
            neg_scores = [float(i.strip()) for i in neg_file.readlines()]

        pos_kde = KernelDensity(kernel="gaussian", bandwidth=0.5).fit(
            np.array(pos_scores).reshape(-1, 1)
        )
        neg_kde = KernelDensity(kernel="gaussian", bandwidth=0.5).fit(
            np.array(neg_scores).reshape(-1, 1)
        )

        # Match the scores with the RNA fragments (Single RNA fragment)
        labels = []
        score_list = []
        kde_score = []

        for i in range(
            len(rna_seq) - (window_size - 1)
        ):  # All the windows starting positions
            score = (
                scores_dict[rna_seq[i : i + window_size]] + 0.89
            )  # Value from ROC-AUC
            score_list.append(score)
            labels.append(rna_seq[i : i + window_size])
            kde_score.append(
                float(
                    np.exp(pos_kde.score_samples(np.array(score).reshape(-1, 1)))
                    / np.exp(neg_kde.score_samples(np.array(score).reshape(-1, 1)))
                )
            )

        min_kde = float(
            np.exp(pos_kde.score_samples(np.array(-1.7 + 0.89).reshape(-1, 1)))
            / np.exp(neg_kde.score_samples(np.array(-1.7 + 0.89).reshape(-1, 1)))
        )
        max_kde = float(
            np.exp(pos_kde.score_samples(np.array(0 + 0.89).reshape(-1, 1)))
            / np.exp(neg_kde.score_samples(np.array(0 + 0.89).reshape(-1, 1)))
        )

        # Normalize the data
        kde_normalized = [(x - min_kde) / (max_kde - min_kde) for x in kde_score]

        my_cmap = plt.cm.get_cmap("RdYlGn")
        colors = my_cmap(kde_normalized)

        # Adjust figure size based on the number of RNA fragments and title length
        height = max(6, len(score_list) * 0.3)  # Adjust height based on number of fragments
        width = 10  # Default width
        
        # Create figure with adjusted size
        fig, ax = plt.subplots(figsize=(width, height))
        y_pos = np.arange(len(score_list))
        ax.barh(y=y_pos, width=score_list, align="center", color=colors)

        # Fix the colorbar issue by properly setting up the ScalarMappable
        sm = ScalarMappable(cmap=my_cmap, norm=plt.Normalize(0, 1))
        sm.set_array([])  # Set an empty array to avoid warning
        cbar = plt.colorbar(sm, ax=ax, pad=0.15)
        cbar.set_label("Confidence score", rotation=270, labelpad=25)

        ax.yaxis.tick_right()
        ax.yaxis.set_label_position("right")
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.set_xlim(x_min, x_max)

        plt.gca().invert_yaxis()
        plt.xlabel("Scores")
        
        # Add title if provided with proper formatting
        if title:
            # Adjust font size for long titles
            title_fontsize = 12 if len(title) > 40 else 14
            
            if wrap_title and len(title) > 40:
                # Split title into multiple lines if it's too long
                words = title.split()
                wrapped_title = []
                current_line = []
                
                for word in words:
                    if len(' '.join(current_line + [word])) <= 40:
                        current_line.append(word)
                    else:
                        wrapped_title.append(' '.join(current_line))
                        current_line = [word]
                
                if current_line:
                    wrapped_title.append(' '.join(current_line))
                
                plt.title('\n'.join(wrapped_title), fontsize=title_fontsize)
            else:
                plt.title(title, fontsize=title_fontsize)
            
            # Add more space at the top for the title
            plt.subplots_adjust(top=0.9)

        return fig

    def find_best_rna(self, rrm_seq):
        # To find the best 5-mer RNA for a rrm_seq
        mer5_list = list(product(*LogoGenerator.NT_LIST * 5))
        # Calculate the scores for all the 3-mer RNA fragments
        mer5_scores = {}
        for rna_seq in mer5_list:
            rna_seq = "".join(rna_seq)
            mer5_scores.update(
                self.score_out_seq(rrm_seq, rna_seq=rna_seq, rna_pos_range=(2, 7))
            )

        sort_scores = dict(
            sorted(mer5_scores.items(), key=lambda x: x[1], reverse=True)
        )

        return sort_scores


class LogoGenerator:
    """
    Set of methods to assess the specificity of any single RRM sequence based on
    RRMScorer:
        1. generate_PPM: Takes all the scores for a given RRM and any RNA seq.
        and the number of top scoring nmers (RNA fragments) to use to calculate
        the PPM (Position Probability Matrix) with the observed probabilities of
        each nucleotide in any of the 5 scored positions.

        2. ppm_to_bits: From the ppm extract the associated bits value for each
        nucleotide in any of the 5 scored positions using the classic equation
        for logo generation. This informs on the information contained in each
        position and in each nucleotide specifically.
            (Optional) 3.1 generate_logo: Takes the bits dataframe as an
            argument to make a logo for that particular RRM (.png). The logo
            depends on the number of nmers used in the previous steps.

        3. retrieve_bits_stats: Return both the total information contained in
        the logo, i.e., the sum of all the values in the dataframe; and the
        maximum bits value for a single RNA motif, i.e., the sum of the highest
        bits value in each position.

    """

    NT_LIST = [["A", "C", "G", "U"]]

    def generate_PPM(self, rna_scores, n_mers, ws=5):
        # PPM = Position Probability Matrix
        ppm = pd.DataFrame(columns=["A", "C", "G", "U"])
        for i in range(ws):
            nt_obs = [mer[i] for mer in list(rna_scores.keys())[:n_mers]]
            freqs = [nt_obs.count(nt) / n_mers for nt in LogoGenerator.NT_LIST[0]]
            # Create a new DataFrame with the freqs values
            new_row = pd.DataFrame(
                {"A": [freqs[0]], "C": [freqs[1]], "G": [freqs[2]], "U": [freqs[3]]}
            )
            # Concatenate the new row to the ppm DataFrame
            ppm = pd.concat([ppm, new_row], ignore_index=True)
        return ppm

    def ppm_to_bits(self, ppm):
        bits_df = pd.DataFrame(columns=["A", "C", "G", "U"])
        for ind in ppm.index:
            bits_factor_A = (
                ppm["A"][ind] * np.log2(ppm["A"][ind]) if not ppm["A"][ind] == 0 else 0
            )
            bits_factor_C = (
                ppm["C"][ind] * np.log2(ppm["C"][ind]) if not ppm["C"][ind] == 0 else 0
            )
            bits_factor_G = (
                ppm["G"][ind] * np.log2(ppm["G"][ind]) if not ppm["G"][ind] == 0 else 0
            )
            bits_factor_U = (
                ppm["U"][ind] * np.log2(ppm["U"][ind]) if not ppm["U"][ind] == 0 else 0
            )

            bits_factor = 2 - np.nansum(
                -bits_factor_A - bits_factor_C - bits_factor_G - bits_factor_U
            )

            new_row = pd.DataFrame(
                {
                    "A": [bits_factor * ppm["A"][ind]],
                    "C": [bits_factor * ppm["C"][ind]],
                    "G": [bits_factor * ppm["G"][ind]],
                    "U": [bits_factor * ppm["U"][ind]],
                }
            )

            # Concatenate the new row to the bits_df DataFrame
            bits_df = pd.concat([bits_df, new_row], ignore_index=True)
        return bits_df

    def generate_logo_to_file(
        self, plot_path, top_scores, n_mers, window_size, dpi=300, title=None, wrap_title=False
    ):
        ppm = self.generate_PPM(rna_scores=top_scores, n_mers=n_mers, ws=window_size)
        bits_df = self.ppm_to_bits(ppm=ppm)
        self.generate_logo(bits_df=bits_df, title=title, wrap_title=wrap_title)
        plt.savefig(plot_path, dpi=dpi)

    def generate_logo(self, bits_df, title=None, wrap_title=False):
        bits_df = bits_df.astype("float64")
        
        # Adjust figure size if there's a title
        if title:
            plt.figure(figsize=(10, 6))
            
        # create Logo object
        ww_logo = logomaker.Logo(bits_df, color_scheme="classic")
        # style using Logo methods
        ww_logo.style_xticks(anchor=0, spacing=1)
        # style using Axes methods
        ww_logo.ax.set_ylabel("Information (bits)")
        ww_logo.ax.set_xlim([-1, len(bits_df)])
        
        # Add title if provided with proper formatting
        if title:
            # Adjust font size for long titles
            title_fontsize = 12 if len(title) > 40 else 14
            
            if wrap_title and len(title) > 40:
                # Split title into multiple lines if it's too long
                words = title.split()
                wrapped_title = []
                current_line = []
                
                for word in words:
                    if len(' '.join(current_line + [word])) <= 40:
                        current_line.append(word)
                    else:
                        wrapped_title.append(' '.join(current_line))
                        current_line = [word]
                
                if current_line:
                    wrapped_title.append(' '.join(current_line))
                
                plt.title('\n'.join(wrapped_title), fontsize=title_fontsize)
            else:
                plt.title(title, fontsize=title_fontsize)
            
            # Add more space at the top for the title
            plt.subplots_adjust(top=0.9)

        return ww_logo



class MatrixPlots:
    def __init__(self):
        self.pkl_dir = "precalculated_scores/pkl_files/"
        self.all_df_dict = self.load_scores(self.pkl_dir)

    def load_scores(self, dir_path):
        df_dict = {}
        for file in glob.glob(dir_path + "*.pkl"):
            df = pd.read_pickle(file)
            res_num = int(file.split("/")[-1].split(".")[0].split("_")[0])
            nuc_num = int(file.split("/")[-1].split(".")[0].split("_")[1])
            df_dict[(res_num, nuc_num)] = df
        return df_dict

    def highlight_cell(self, x, y, ax=None, **kwargs):
        self.rect = plt.Rectangle(
            (x - 0.5, y - 0.5), 1, 1, fill=False, **kwargs, clip_on=False
        )
        ax = ax or plt.gca()
        ax.add_patch(self.rect)
        return self.rect

    def plot_all_dfs(self):
        # Iterate over files in the directory
        for res_nuc_pos, df in self.all_df_dict.items():
            print(res_nuc_pos)
            # Generate the matshow plots for the individual positions
            if df.empty == False:
                df = df.dropna(axis=0, thresh=1)
                df = df.round(decimals=2)
                pos, rna_pos = res_nuc_pos[0], res_nuc_pos[1]

                _max = 3
                _min = -3
                fig = plt.figure()
                ax1 = plt.subplot()
                norm = mcolors.TwoSlopeNorm(vmin=_min, vmax=_max, vcenter=0)

                df = df.astype("float").round(decimals=2)

                ax1.matshow(df, cmap=plt.cm.RdBu, aspect="auto", norm=norm)

                for i, x in zip(df.index, range(df.shape[0] + 1)):
                    for j, y in zip(df.columns, range(df.shape[1])):
                        c = df.loc[i][j]
                        if abs(c) > 0.7 * _max:
                            ax1.text(
                                y,
                                x,
                                str(c),
                                va="center",
                                ha="center",
                                color="white",
                                fontsize=12,
                            )
                        else:
                            ax1.text(
                                y,
                                x,
                                str(c),
                                va="center",
                                ha="center",
                                color="black",
                                fontsize=12,
                            )

                # Df general data
                xaxis = np.arange(df.shape[1])
                yaxis = np.arange(df.shape[0])
                ax1.set_xticks(xaxis)
                ax1.set_yticks(yaxis)
                ax1.set_ylabel("Neighbour residues")
                ax1.set_xlabel("RNA nucleotide")
                ax1.set_xticklabels(df.columns, fontsize=12)
                ax1.set_yticklabels(df.index, fontsize=12)
                plt.title("Prot -> {} - RNA -> {}".format(pos, rna_pos), fontsize=14)

                all_combinations = list(itertools.product(df.index, df.columns))
                for res, nuc in all_combinations:
                    if nuc == "No_contact":
                        continue
                    # Get the row index based on the row name
                    row_index = df.index.get_loc(res)
                    # Get the column index based on the column name
                    column_index = df.columns.get_loc(nuc)
                    self.highlight_cell(
                        column_index, row_index, color="yellow", linewidth=3, zorder=10
                    )
                    plt.savefig(
                        "precalculated_scores/png_files/"
                        "{}_{}_highlighted_{}_{}.png".format(pos, rna_pos, res, nuc)
                    )
                    self.rect.set_visible(False)
