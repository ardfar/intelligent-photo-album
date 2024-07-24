import requests

class Hashtag:
    @staticmethod
    def generate_hashtags(keyword):
        url = "https://hash-tag-generator.p.rapidapi.com/get_has_tags"

        querystring = {"query":keyword,"language":"en"}

        headers = {
            "x-rapidapi-key": "9622d49abdmsh9442281ea7db4f8p16f335jsn88698824b638",
            "x-rapidapi-host": "hash-tag-generator.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        return response.json()