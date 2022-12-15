import numpy as np
import random, time, pylsl
from time import sleep
from pylsl import StreamInfo, StreamOutlet, StreamInlet, resolve_streams

def main():
    info = StreamInfo('MyMarkerStream', 'Markers', 1, 0, 'string', 'myuidw43536')

    streams = pylsl.resolve_streams(wait_time=3.)
    inlet = []
    for stream in streams:
        name = pylsl.StreamInlet(stream).info().name() 
        print(name)
        if (name == "RValues"):
            inlet = pylsl.StreamInlet(stream)

    outlet = StreamOutlet(info)

    UP = 'UP'
    DOWN = 'DOWN'
    high = 0.25                                          #閾値の設定
    low = 0.25
    inlet.open_stream()                                  # バッファ開始
    sleep(.1)                                            # バッファにある程度データをためる

    while True:
         # データ取得
        if True:
            d, _ = inlet.pull_chunk(max_samples=1024)    # バッファにあるデータを全部取る
            assert(len(d) < 1024)                        # 念のため、全部取り切れていることを確認する
            try:
                sample = np.array(d)[-1,1]               # とってきたデータの最後の部分を使う
            except:                                      # サンプリングレートが落ちてバッファが空になることもあるので...
                pass                                     # その時はpassしてごまかす
        print(sample)

        #閾値に応じて文字列を出力
        if(sample > high):
           outlet.push_sample([UP])
        if(sample < high):
            outlet.push_sample([DOWN])
        time.sleep(3)

if __name__ == '__main__':
    main()
