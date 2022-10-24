#FETCHING LIKES AND DISLIKES FROM YT VIDEOS
#WITH THE HELP FROM "Returnyoutubedislike.com"
import requests
import re

def get_scores(id):
    r = requests.get(f"https://returnyoutubedislikeapi.com/votes?videoId={id}")
    txt = r.text

    likes, dislikes = int(re.findall('(?<="likes":).[0-9]+',txt)[0]),int(re.findall('(?<="dislikes":).[0-9]+',txt)[0])

    return likes,dislikes
def main():
    id = "kqJuzLbIt4g"
    likes, dislikes = get_scores(id)

    print(f"The video with id '{id}' has:")
    print(f"Likes : {likes}")
    print(f"Dislikes : {dislikes}")

if __name__ == "__main__":
    main()
