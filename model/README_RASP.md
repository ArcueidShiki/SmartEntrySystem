# Install Tensorflow and OpenCV on Raspberry PI

## Check system info

```bash
cat /etc/os-release
uname- m # armv7l
```

```bash
sudo apt update && sudo apt upgrade
```

## Install python 3.7

Since Raspberry Pi cannot directory install the tensorflow and opencv, we need do following steps. Install tensorflow from a [.whl](https://github.com/PINTO0309/Tensorflow-bin/blob/main/previous_versions/download_tensorflow-2.4.0-cp37-none-linux_armv7l.sh) file.

![alt text](image.png)

where `cp` means cpython version.

```bash
python3 -V

curl https://pyenv.run | bash

sudo nano ~/.bashrc
```

Open the `.bashrc` file, navigate to the end and add the following three lines, then save and exit.

```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
```

Then execute:
```bash
exec $SHELL

pyenv update
pyenv install --list
pyenv install 3.7.6
cd project_directory
pyenv local 3.7.6

python -m virutalenv env
source env/bin/activate

```

download the tensorflow .whl file from this [link](https://drive.google.com/uc?export=download&id=1dKQCz4CA0rz2utt0GmXEQWnIeQ4SxHO5)

```bash
pip install tensorflow-2.4.0-cp37-none-linux_armv7l.whl


sudo apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev gcc gfortran libgfortran5 libatlas3-base libatlas-base-dev libopenblas-dev libopenblas-base libblas-dev liblapack-dev cython3 libatlas-base-dev openmpi-bin libopenmpi-dev python3-dev build-essential cmake pkg-config libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libhdf5-serial-dev libhdf5-103 libqt5gui5 libqt5webkit5 libqt5test5 python3-pyqt5

pip install opencv-contrib-python
```

Test
```python
import tensorflow as tf
tf.__version__
```