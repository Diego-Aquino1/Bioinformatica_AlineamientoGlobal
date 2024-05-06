class NeedlemanWunsch:
    def __init__(self, seq1, seq2, match_score=1, mismatch_score=-1, gap_penalty=-2):
        # Inicialización de las secuencias y puntajes
        self.seq1 = seq1
        self.seq2 = seq2
        self.match_score = match_score
        self.mismatch_score = mismatch_score
        self.gap_penalty = gap_penalty
        
        # Dimensiones de las secuencias
        self.m = len(seq1)
        self.n = len(seq2)
        
        # Matrices de puntuación y traceback
        self.score_matrix = [[0] * (self.n + 1) for _ in range(self.m + 1)]
        self.traceback_matrix = [[[] for _ in range(self.n + 1)] for _ in range(self.m + 1)]
        
        # Lista para almacenar las alineaciones óptimas
        self.alignments = []

    def align(self):
        # Método para realizar el alineamiento
        self.initialize_matrices()
        self.fill_matrices()
        self.traceback(self.m, self.n, '', '')
        self.write_results()

    def initialize_matrices(self):
        # Inicialización de las matrices de puntuación y traceback
        for i in range(1, self.m + 1):
            self.score_matrix[i][0] = self.score_matrix[i - 1][0] + self.gap_penalty
            self.traceback_matrix[i][0] = [(i - 1, 0)]
        for j in range(1, self.n + 1):
            self.score_matrix[0][j] = self.score_matrix[0][j - 1] + self.gap_penalty
            self.traceback_matrix[0][j] = [(0, j - 1)]

    def fill_matrices(self):
        # Llenado de las matrices de puntuación y traceback
        for i in range(1, self.m + 1):
            for j in range(1, self.n + 1):
                # Cálculo de los puntajes para cada posible movimiento
                match = self.score_matrix[i - 1][j - 1] + (self.match_score if self.seq1[i - 1] == self.seq2[j - 1] else self.mismatch_score)
                delete = self.score_matrix[i - 1][j] + self.gap_penalty
                insert = self.score_matrix[i][j - 1] + self.gap_penalty
                max_score = max(match, delete, insert)
                self.score_matrix[i][j] = max_score
                
                # Actualización de la matriz de traceback con las coordenadas previas que condujeron al puntaje máximo
                if match == max_score:
                    self.traceback_matrix[i][j].append((i - 1, j - 1))
                if delete == max_score:
                    self.traceback_matrix[i][j].append((i - 1, j))
                if insert == max_score:
                    self.traceback_matrix[i][j].append((i, j - 1))

    def traceback(self, i, j, alignment1, alignment2):
        # Recorrido para encontrar todas las alineaciones óptimas
        if i == 0 and j == 0:
            self.alignments.append((alignment1[::-1], alignment2[::-1]))
            return
        for prev_i, prev_j in self.traceback_matrix[i][j]:
            if (prev_i, prev_j) == (i - 1, j - 1):
                self.traceback(prev_i, prev_j, alignment1 + self.seq1[i - 1], alignment2 + self.seq2[j - 1])
            elif (prev_i, prev_j) == (i - 1, j):
                self.traceback(prev_i, prev_j, alignment1 + self.seq1[i - 1], alignment2 + '-')
            elif (prev_i, prev_j) == (i, j - 1):
                self.traceback(prev_i, prev_j, alignment1 + '-', alignment2 + self.seq2[j - 1])

    def write_results(self):
        # Escritura de los resultados en un archivo
        with open("alignment_results.txt", "w") as file:
            # Escribir la matriz de puntuación
            file.write("Score Matrix:\n")
            for row in self.score_matrix:
                file.write("\t".join(map(str, row)) + "\n")
            
            # Escribir el puntaje final
            final_score = self.score_matrix[self.m][self.n]
            file.write("\nFinal Score: {}\n".format(final_score))
            
            # Escribir el número de alineaciones óptimas
            num_alignments = len(self.alignments)
            file.write("Number of Optimal Alignments: {}\n".format(num_alignments))
            
            # Escribir las alineaciones óptimas
            file.write("\nOptimal Alignments:\n")
            for i, alignment in enumerate(self.alignments):
                file.write("Alignment {}:\n".format(i + 1))
                file.write(alignment[0] + "\n")
                file.write(alignment[1] + "\n\n")

        print("Results written to alignment_results.txt")

# Ejemplo de uso
seq1 = "ACTGATTCA"
seq2 = "ACGCATCA"
seq3 = "HEAGWAGHEE"
seq4 = "PAWHEAE"
nw = NeedlemanWunsch(seq1, seq2)
#nw = NeedlemanWunsch(seq3, seq4)
nw.align()
