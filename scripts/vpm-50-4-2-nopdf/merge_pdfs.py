import sys
import os

def create_latex_document(input_files, output_file):
    with open('temp_latex.tex', 'w') as f:
        f.write("\\documentclass{article}\n")
        f.write("\\usepackage[margin=1in]{geometry}\n")
        f.write("\\usepackage{pdfpages}\n")
        f.write("\\usepackage{graphicx}\n")
        f.write("\\begin{document}\n")

        for pdf in input_files:
            f.write("\\includegraphics[width=0.24\\textwidth]{" + pdf + "}\n")
            f.write("\\quad\n")  # Adjust spacing as needed

        f.write("\\end{document}\n")

    os.system("pdflatex -jobname=" + output_file + " temp_latex.tex")
    os.system("rm temp_latex.tex temp_latex.log temp_latex.aux")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python merge_pdfs.py output input1.pdf input2.pdf [...]")
    else:
        output_pdf_name = sys.argv[1]
        input_pdf_files = sys.argv[2:]
        create_latex_document(input_pdf_files, output_pdf_name)
