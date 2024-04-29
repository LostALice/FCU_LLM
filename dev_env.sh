apt install python3.11 -y

# init pythen venv
py -3.11 -m venv . 

# enter venv
source bin/activate

# install packages
python.exe -m pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -r ./req.txt