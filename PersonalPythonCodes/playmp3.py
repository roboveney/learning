import subprocess

def play_mp3(path):
    subprocess.Popen(['mpg123', '-q', path]).wait()
    
play_mp3('welcome.wav')
