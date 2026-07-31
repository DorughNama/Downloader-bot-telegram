import yt_dlp

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse


app = FastAPI(
    title="Instagram Direct Stream API",
    version="5.0"
)



@app.get("/")
def home():

    return {

        "status": "online",

        "service": "Instagram Direct Stream"

    }





@app.get("/stream")
def stream(

    url: str = Query(...)

):


    if "instagram.com" not in url:


        return JSONResponse(

            {

                "status": "error",

                "detail":

                "Only Instagram links are supported"

            }

        )



    try:


        options = {


            "format":

            "best",


            "quiet":

            True,


            "noplaylist":

            True,


            "nocheckcertificate":

            True,


            "http_headers":

            {

                "User-Agent":

                "Mozilla/5.0"

            }

        }




        with yt_dlp.YoutubeDL(options) as ydl:


            info = ydl.extract_info(

                url,

                download=False

            )



            video_url = info.get(

                "url"

            )



            title = info.get(

                "title",

                "Instagram Video"

            )



            quality = info.get(

                "height",

                "Original"

            )



            duration = info.get(

                "duration",

                0

            )




        return {


            "status":

            "success",


            "title":

            title,


            "quality":

            str(quality),


            "duration":

            duration,


            "video_url":

            video_url


        }





    except Exception as e:



        return JSONResponse(

            {


                "status":

                "error",


                "detail":

                str(e)

            }

        )