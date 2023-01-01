import os
import subprocess

# Set the installation directory
install_dir = '/opt/intel'
openvino_version = '2022.3.0'
openvino_dir = install_dir + "/openvino"
# Create the installation directory if it doesn't exist
if not os.path.exists(install_dir):
    subprocess.run(['sudo', 'mkdir', '-p', install_dir])

# Go to the downloads directory
os.chdir(os.path.expanduser('~/Downloads'))

# Download the OpenVINO Runtime archive file for Raspberry Pi
subprocess.run(['wget', 'https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.3/linux/l_openvino_toolkit_debian9_2022.3.0.9052.9752fafe8eb_armhf.tgz', '-O', 'openvino_' + openvino_version + '.tgz'])

# Extract the archive file and move it to the installation directory
subprocess.run(['sudo', 'tar', '-xf', 'openvino_' + openvino_version + '.tgz'])
subprocess.run(['sudo', 'mv', 'l_openvino_toolkit_debian9_' + openvino_version + '.9052.9752fafe8eb_armhf', install_dir + '/openvino_' + openvino_version])

# Install required system dependencies on Linux
subprocess.run(['sudo', '-E', install_dir + '/openvino_' + openvino_version + '/install_dependencies/install_openvino_dependencies.sh'])

# Create a symbolic link for easy access
subprocess.run(['sudo', 'ln', '-s', 'openvino_' + openvino_version, install_dir + '/openvino'])

# Add the environment variables to .bashrc
bashrc_path = os.path.expanduser('~/.bashrc')
with open(bashrc_path, 'a') as f:
    f.write('\n')
    f.write('# Set the environment variables for OpenVINO\n')
    f.write('source ' + openvino_dir + '/setupvars.sh\n')

# Source .bashrc to set the environment variables for the current terminal session
subprocess.run(['source', bashrc_path])

# Install CMake
subprocess.run(['sudo', 'apt', 'install', 'cmake'])

print('OpenVINO Runtime for Raspbian OS has been installed successfully!')

# Add the current user to the users group
subprocess.run(['sudo', 'usermod', '-a', '-G', 'users', '"$(whoami)"'])

# Set the OpenVINO installation directory
openvino_dir = '/opt/intel/openvino'


# Check if the 97-myriad-usbboot.rules file exists in /etc/udev/rules.d/
if not os.path.exists('/etc/udev/rules.d/97-myriad-usbboot.rules'):
    # If the file does not exist, create it with the necessary content
    with open('/etc/udev/rules.d/97-myriad-usbboot.rules', 'w') as f:
        f.write('SUBSYSTEM=="usb", ATTRS{idProduct}=="2150", ATTRS{idVendor}=="03e7", GROUP="users", MODE="0660", ENV{ID_MM_DEVICE_IGNORE}="1"\n')
        f.write('SUBSYSTEM=="usb", ATTRS{idProduct}=="2485", ATTRS{idVendor}=="03e7", GROUP="users", MODE="0660", ENV{ID_MM_DEVICE_IGNORE}="1"\n')
        f.write('SUBSYSTEM=="usb", ATTRS{idProduct}=="f63b", ATTRS{idVendor}=="03e7", GROUP="users", MODE="0660", ENV{ID_MM_DEVICE_IGNORE}="1"\n')

# Install the USB rules for the Intel Neural Compute Stick 2
subprocess.run(['sh', openvino_dir + '/install_dependencies/install_NCS_udev_rules.sh'])

# (Optional) Build and run the Image Classification sample to verify the installation

# Navigate to a directory and create a build directory
os.chdir(os.path.expanduser('~'))
subprocess.run(['mkdir', 'build', '&&', 'cd', 'build'])

# Build the Hello Classification Sample
subprocess.run(['cmake', '-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_CXX_FLAGS="-march=armv7-a"', openvino_dir + '/samples/cpp'])
subprocess.run(['make', '-j2', 'hello_classification'])

# Download the pre-trained squeezenet1.1 image classification model
subprocess.run(['git', 'clone', '--depth', '1', 'https://github.com/openvinotoolkit/open_model_zoo'])
os.chdir('open_model_zoo/tools/model_tools')
subprocess.run(['python3', '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.run(['python3', '-m', 'pip', 'install', '-r', 'requirements.in'])
subprocess.run(['python3', 'downloader.py', '--name', 'squeezenet1.1'])

# # Set the path to the input image and model
# image_path = '<path_to_image>'
# model_path = '<path_to_model>/squeezenet1.1.xml'

# # Run the sample specifying the model and VPU required to run with the Raspbian OS
# subprocess.run(['./armv7l/Release/hello_classification', model_path, image_path, 'MYRIAD'])

print('Dependencies for using the Intel Neural Compute Stick 2 on Raspbian OS have been installed successfully!')