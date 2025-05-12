import furet.app
from furet import repository, crawler

#from datetime import datetime

def main():
    crawler.init()
    repository.setup()  
    # traitement = Traitement()
    # traitement_thread = threading.Thread(target=traitement.startTraitement)
    # traitement_thread.start()
    furet.app.main()

if __name__ == '__main__':
    main()
    