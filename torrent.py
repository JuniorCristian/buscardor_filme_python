import libtorrent as lt
import time
import datetime
import telegrambot


def download(url, type, mensagem):
    ses = lt.session()
    ses.listen_on(6881, 6891)

    params = {
        'save_path': '/home/cristian/Documentos',
        'storage_mode': lt.storage_mode_t(2),
        # 'paused': False,
        # 'auto_managed': True,
        # 'duplicate_is_error': True
    }

    print(url)

    handle = lt.add_magnet_uri(ses, url, params)
    ses.start_dht()

    begin = time.time()
    print(datetime.datetime.now())

    print('Baixando Metadata')
    while (not handle.has_metadata()):
        time.sleep(1)

    print('Sucesso, Baixando torrent')
    print('Começando', handle.name())

    while (handle.status().state != lt.torrent_status.seeding):
        s = handle.status()

        texto = ('Seu Download está %.2f %% completo (down: %.1f Kb/s up: %.1f Kb/s pares: %d)' % (
        s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers))

        telegrambot.atualizacaoStatus(mensagem, texto)

        time.sleep(50)
    ses.stop_dht()
    end = time.time()
    print(handle.name(), "COMPLETED")
    print("Elapsed Time", int((end - begin) // 60), "min: ", int((end - begin) % 60), "sec: ")
    print(datetime.datetime.now())
    telegrambot.atualizacaoStatus(mensagem, ("Tempo de download: "+str(int((end - begin) // 60))+ "min"+str(int((end - begin) % 60))+"sec"))