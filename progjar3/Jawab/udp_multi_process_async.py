import time
import datetime
import socket
import logging
from multiprocessing import Process, Pool

TARGET_IP = "192.168.122.245"
TARGET_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT, 1)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST, 1)

def image():
    lists = dict()
    lists['ITS'] = 'ITS.png'
    lists['Background'] = 'Background.jpg'
    return lists

def broadcast():
    f = open(fname, 'rb')
    img = f.read()
    sock.sendall(img)
    print(f"Sending Image {fname}")

    # Look for the response
    amount_received = 0
    amount_expected = len(img)
    with sock, open(rname, 'wb') as file:
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            if not data:
                break
            file.write(data)

def download_semua():
    texec = dict()
    daftar = image()
    status_task = dict()

    # 2 task yang dapat dikerjakan secara simultan, dapat diset sesuai jumlah core
    task_pool = Pool(processes=20)
    catat_awal = datetime.datetime.now()
    for k in daftar:
        print(f"mendownload {daftar[k]}")
        #bagian ini merupakan bagian yang mengistruksikan eksekusi fungsi download gambar secara multiprocess
        texec[k] = task_pool.apply_async(func=broadcast, args=(daftar[k],))

    #setelah menyelesaikan tugasnya, dikembalikan ke main process dengan mengambil hasilnya dengan get
    for k in lists:
        status_task[k]=texec[k].get(timeout=10)

    catat_akhir = datetime.datetime.now()
    selesai = catat_akhir - catat_awal
    print(f"Waktu TOTAL yang dibutuhkan {selesai} detik {catat_awal} s/d {catat_akhir}")
    print("status TASK")
    print(status_task)


#fungsi download_gambar akan dijalankan secara multi process
#if __name__=='__main__':
#    download_semua()