import rclpy, tempfile, os, wave, pyaudio
from std_msgs.msg import String
from aip import AipSpeech          # 百度 REST，零样本
client = AipSpeech('7336787','fjSvqHvsX8bPI4MAT2wK1sv7','8aIOwqzwI5gULzRBpQE7iQE0m2nniGOH')

RATE, CHUNK = 16000, 1024
def record_3s(fname):
    p = pyaudio.PyAudio()
    s = p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,frames_per_buffer=CHUNK)
    frames = [s.read(CHUNK) for _ in range(int(RATE/CHUNK*3))]
    s.close(); p.terminate()
    with wave.open(fname,'wb') as w:
        w.setnchannels(1); w.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        w.setframerate(RATE); w.writeframes(b''.join(frames))

def main():
    rclpy.init()
    node = rclpy.create_node('asr_jazzy')
    pub = node.create_publisher(String, 'voice_words', 10)
    while rclpy.ok():
        with tempfile.NamedTemporaryFile(suffix='.wav',delete=False) as tmp:
            record_3s(tmp.name)
            with open(tmp.name,'rb') as f: res=client.asr(f.read(),'wav',16000,{'dev_pid':1537})
            os.remove(tmp.name)
            if res['err_no']==0:
                txt=res['result'][0].strip()
                node.get_logger().info(f'ASR:{txt}')
                pub.publish(String(data=txt))
        rclpy.spin_once(node,timeout_sec=0.5)

if __name__=='__main__': main()
