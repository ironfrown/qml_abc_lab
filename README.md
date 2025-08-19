# Quantum Machine Learning A-B-C in Qiskit
- **Author:** [Jacob Cybulski](https://jacobcybulski.com/) ([LinkedIn](https://www.linkedin.com/in/jacobcybulski/)), *Enquanted*
- **Associated with:** [QPoland](https://qworld.net/qpoland/)
- **Aims:** To explore the creation and use of quantum machine learning models in Qiskit.
- **Description:**
  This QML ABC lab explores the process of developing a simple quantum model in Qiskit.<br>
  The lab includes three practical sessions that cover the QML concepts, models, and techniques.<br>
  The first introductory lab will be demonstrated by the presenter.<br>
  The second lab is designed to be completed by the participants and its tasks discussed on Discord.<br>
  The final lab is a challenge, to be undertaken by the participants themselves.
- **Creation Date:**<br>
  October 1, 2022: Initial development<br>
  August 24, 2025: Presented to [QBronze-167 Workshop](https://qworld.net/qbronze167/)
- **How to cite this work:**<br>
  If you are a researcher and wanted to use these resources, please cite my work as follows.<br>

  _**The presentation (slides and video once available):**_<br>
  Jacob L. Cybulski, "Quantum Algorithms and Data Encoding for QML with Qiskit",<br>
  QBronze-167 Workshop by QIndia / QWorld, August 9-10 and 23-24, 2025,<br>
  [https://jacobcybulski.com/seminars/slides/2025_QIndia_QML_ABC_v1_1.pdf](https://jacobcybulski.com/seminars/slides/2025_QIndia_QML_ABC_v1_1.pdf).<br>

  _**This GitHub:**_<br>
  Jacob L. Cybulski (ironfrown), "Quantum Machine Learning A-B-C in Qiskit",<br>
  GitHub, 2025,
  [https://github.com/ironfrown/qml_abc_lab/](https://github.com/ironfrown/qml_abc_lab/),
  Accessed Day-Month-Year.

## Folders
This site is structured as follows:
- _**dev:**_ developement versions of the three labs notebooks
- _**runs:**_ answers to all tasks set in the labs, except for:
  - Lab 2 (Homework): answers to tasks G and H have not been provided
  - Lab 3 (Challenge): answers to tasks B and C have not been provided 
- _**slides:**_ presentation slides in PDF (as they become available)
- _**legacy:**_ previous versions of files (in case you really really wanted them)
  
## Important notebooks

You can play with these notebooks implementing QML curve-fitting models in Qiskit, enjoy!<br>
Their simplicity is misleading as the tasks set by these labs will make you sweat.<br>
Note however that these notebooks may be updated at any time!

<table style="float: left;">
    <tr><th style="text-align: left;">Notebook</th>
        <th style="text-align: left;">Dataset</th>
        <th style="text-align: left;">Model</th>
        <th style="text-align: left;">Description</th>
    </tr>
    <tr><td style="vertical-align: top;"><strong><em>qml_abc_01_sin</em></strong></td>
        <td style="vertical-align: top;">sin_n100</td>
        <td style="vertical-align: top;">qnn_model_1</td>
        <td style="vertical-align: top;">A simple QML model trained on very simple "sine" function.</td>
    </tr>
    <tr><td style="vertical-align: top;"><strong><em>qml_abc_02_sinful</em></strong></td>
        <td style="vertical-align: top;">sinful_n100</td>
        <td style="vertical-align: top;">qnn_model_2</td>
        <td style="vertical-align: top;">An evil twist in a trig "sinful" data makes the previous model unworkable.<br>
                                         On QML portals typical advice is make the model more "expressive".<br>
                                         He he he, they never give their code solution to help you out!</td>
    </tr>
    <tr><td style="vertical-align: top;"></td>
        <td style="vertical-align: top;">sinless_n100</td>
        <td style="vertical-align: top;">qnn_model_2</td>
        <td style="vertical-align: top;">Once we fix the "sinful" model, this new "sinless" dataset will wreck it.</td>
    </tr>
    <tr><td style="vertical-align: top;"><strong><em>qml_abc_03_mglass</em></strong></td>
        <td style="vertical-align: top;">mackie_glass</td>
        <td style="vertical-align: top;">qnn_model_3</td>
        <td style="vertical-align: top;">The challenge exercise is to create a Qiskit model for Mackie-Glass data.</td>
    </tr>
</table><div style="clear: both;"></div>
            
## Requirements
This repository requires Qiskit v1.4.4 and Qiskit ML 0.8.3.<br>
at the development time Qiskit ML was incompatible with Qiskit v2.0+.

- Create a Qiskit conda environment and activate it<br>
    conda create -n qiskit-qml python=3.11<br>
    conda activate qiskit-qml
- install the Qiskit package, which includes ML:<br>
    pip install qiskit[visualization]==1.4.4<br>
    pip install qiskit-ibm-runtime<br>
    pip install qiskit-aer or pip install qiskit-aer-gpu<br>
    pip install qiskit-machine-learning ==0.8.3
- The following packages would have been installed as well:<br>
    numpy matplotlib pandas pillow rustworkx scipy scikit-learn seaborn
- Additional packages often used:<br>
    pip install jupyter jupyterlab <br>
    conda install freetype 
- Run jupyter or jupyter lab

All code was tested on Ubuntu 22.04-24.04.

## License
This project is licensed under the [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.en.html).<br>
The GPL v3 license requires attribution for modifications and derivatives,<br>
ensuring that users know which versions are changed and to protect the reputations of original authors.