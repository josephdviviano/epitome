# link up all users to grandvizier's profile (ease of maintenance)
for s in /home/*; do sudo ln -s /home/grandvizier/.bashrc ${s}/.bashrc; done