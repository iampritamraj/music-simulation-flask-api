# Implemented two api 
    ## download and save music in mongodb

        # sample url: http://127.0.0.1:8090/upload?audioType=song&audioId=2&audioUrl=https://vipsongs.xyz/singles/Stebin%20Ben/Main%20Marjaunga%20-%20Stebin%20Ben.mp3&audioName=Main Marjaunga

            # POST http://127.0.0.1:8090/upload?audioType=song&audioId=3&audioName=Main Marjaunga&audioUrl=https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3
    
    ## Retrive music fro mongodb and stream live 
        # sample url: http://127.0.0.1:8090/fetchAudio?audioType=song&audioId=2

            # GET http://127.0.0.1:8090/fetchAudio?audioType=song&audioId=1