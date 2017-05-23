# GITR Viewer

Every year, the World Economic Forum is writing its "Global Information Technology Report" (GITR) in which country are rated and ranked accordingly to their ability to "embrace this new digital era" and integrate ICT in their economy.


This tool allow you to draw a Chloropeth Map of the World from any index / pillar / category of the Networked Readiness Index (NRI) that you want to investigate.


You can either run the tool in your own Jupyter Notebook, or use the NBViewer link [here](https://nbviewer.jupyter.org/github/AlexConnat/GITR-Viewer/blob/master/MAIN.ipynb).


The function `plot_map_for_indicator()` accepts :
- Any indicator `1.01`, `1.02`, ..., `10.04`
- One of the four indexes (A: Environement, B: Readiness, C: Usage, D: Impact) `"A"`, `"B"`, `"C"` or `"D"`
- One of the 10 pillars : `A.01`, `A.02`, `B.03`, ..., `D.10`
- The global Networked Readiness Index `"NRI"`


For further details and explanations of the indices : <a href="http://reports.weforum.org/global-information-technology-report-2016/economies/#economy=CHE">http://reports.weforum.org/global-information-technology-report-2016/economies/#economy=CHE</a>
