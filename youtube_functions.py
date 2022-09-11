from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class Youtube:
    def __init__(self, Name):
        driver_path = r'C:\Users\Aman\PycharmProjects\youtube_scrapping\chromedriver.exe'
        options = Options()
        options.headless = False
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.Name = Name

    def execute_browser(self, exicute=""):
        time.sleep(1)
        self.driver.get(exicute)

    def channel_url(self):
        try:
            base_url = "https://www.youtube.com"
            keyword = self.Name
            self.driver.get(f"{base_url}/search?q={keyword}")
            channel_name = self.driver.find_element_by_xpath('//*[@id="avatar-section"]/a')
            link = channel_name.get_attribute('href')
            time.sleep(1)
            l = str(link)
            x = l.split("/")
            self.channel_id = x[4]
            return link

        except Exception:
            return "Try again"

    def channel_videos(self):
        videos = f"{self.channel_url()}/videos"
        time.sleep(1)
        return videos

    def channel_videos_link(self):
        try:
            hrefs = [video.get_attribute('href') for video in self.driver.find_elements_by_id("thumbnail")]
            links = []
            for href in hrefs:
                links.append(href)
            return links

        except Exception as e:
            hrefs = [video.get_attribute('href') for video in self.driver.find_elements_by_id("thumbnail")]
            links = []
            for href in hrefs:
                links.append(href)
            # print(links)
            return links

    # def video_details(self):
    #     links = self.channel_videos_link()
    #     print(links[10])
    #     time.sleep(1)
    #     self.driver.get(links[10])

    def filter_links(self):
        list_link = self.channel_videos_link()
        link = []
        for i in list_link:
            if i != None:
                link.append(i)
        list_of_links = []
        shorts = []
        for i in link:
            x = i.split("/")
            if x[3] == 'shorts':
                shorts.append(i)
            else:
                list_of_links.append(i)
        return list_of_links

    def scroll_me(self, value_up=0, value_down=0):
        time.sleep(1.5)
        self.driver.execute_script(f"window.scrollTo({value_up},{value_down});")

    def scroll_down(self):
        time.sleep(3)
        while True:
            scroll_height = 2000
            document_height_before = self.driver.execute_script("return document.documentElement.scrollHeight")
            self.driver.execute_script(f"window.scrollTo(0, {document_height_before + scroll_height});")
            time.sleep(1.5)
            document_height_after = self.driver.execute_script("return document.documentElement.scrollHeight")
            if document_height_after == document_height_before:
                break

    def video_comments(self):
        # list_of_links = self.channel_videos_link()
        # link = list_of_links[60]
        # self.execute_browser(link)
        # time.sleep(5)
        # self.scroll_me(value_down=600)
        # time.sleep(2)
        # self.scroll_me(value_up=500)
        # time.sleep(2)
        # self.scroll_me(value_down=600)

        comments = []
        for item in self.driver.find_elements_by_class_name("style-scope ytd-comment-renderer"):
            # print(item.text)
            comments.append(item.text)
            # print("-" * 80)
        key = []
        value = []
        for i in comments:
            x = i.split("\n")
            key.append(x[0])
            value.append(x[2])
        dt = {key[i]: value[i] for i in range(len(key))}
        # print(dt)
        return dt

    def video_likes(self):
        # list_of_links = self.channel_videos_link()
        # link = list_of_links[60]
        # self.execute_browser(link)
        likes = self.driver.find_element_by_css_selector(
            'yt-formatted-string[class="style-scope ytd-toggle-button-renderer style-text"]').text
        if likes == "":
            likes = self.driver.find_element_by_css_selector(
                'yt-formatted-string[class="style-scope ytd-toggle-button-renderer style-text"]').text
        # print(likes)
        return likes

    def video_comment_views_number(self):
        # list_of_links = self.channel_videos_link()
        # link = list_of_links[50]
        # self.execute_browser(link)
        # time.sleep(3)
        # self.scroll_me(value_down=600)
        # time.sleep(2)
        total_comments = self.driver.find_elements_by_id('count')
        x = []
        for i in total_comments:
            # print(i.text)
            x.append(i.text)

        # Spitting the list to check comments is loaded or not(present)
        for i in x:
            y = i.split(" ")
        # If comments is not in the list then re-run the same code
        if "Comments" not in y:
            total_comments = self.driver.find_elements_by_id('count')
            x = []
            for i in total_comments:
                print(i.text)
                x.append(i.text)
        comments = x[2]
        views = x[1]
        # print(comments, views)
        return comments, views

    def video_title(self):
        # list_of_links = self.channel_videos_link()
        # link = list_of_links[50]
        # self.execute_browser(link)
        # time.sleep(3)
        # self.scroll_me(value_down=600)
        # time.sleep(2)
        title = self.driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
        if title == "":
            title = self.driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
        # print(title)
        return title

    def video_thumbnail(self, link):
        # list_of_links = self.channel_videos_link()
        # link = list_of_links[50]
        # self.execute_browser(link)
        # time.sleep(3)
        # self.scroll_me(value_down=600)
        # time.sleep(2)
        s = str(link)
        match = s.split('=')
        thumbnail = "https://i1.ytimg.com/vi/" + match[1] + "/hqdefault.jpg"
        # print(thumbnail)
        return thumbnail

    def video_downloader(self, link):
        # list_of_links = self.channel_videos_link()
        # link = list_of_links[50]
        # self.execute_browser(link)
        # time.sleep(3)
        # self.scroll_me(value_down=600)
        # time.sleep(2)
        try:
            l = link.split("/")
            l1 = [i.replace('www.youtube.com', 'www.ssyoutube.com') for i in l]
            l = "/".join(l1)
            self.execute_browser(l)
            download = self.driver.find_element_by_xpath(
                '//*[@id="sf_result"]/div/div/div[2]/div[2]/div[1]/a').get_attribute('href')
            print("Click on this link to download from the browser :", download)

        except Exception:
            download = "No downloads Available"
            print(download)

        return download

    def extract_everything_from_video(self, video_number=10):
        try:
            self.execute_browser(self.channel_videos())
            self.scroll_me(value_down=1500)
            time.sleep(2)
            self.scroll_me(value_down=15000)
            time.sleep(2)
            list_of_links = self.filter_links()
            link = list_of_links[video_number]
            self.execute_browser(link)
            time.sleep(3)
            self.scroll_me(value_down=600)
            time.sleep(1)
            self.scroll_me(value_up=600)
            time.sleep(1)
            self.scroll_down()

            # self.scroll_me(value_down=1500)
            # time.sleep(1)
            # self.scroll_me(value_down=15000)
            # time.sleep(1)
            # self.scroll_me(value_down=15000)
            title = self.video_title()
            likes = self.video_likes()
            comments_number, video_view = self.video_comment_views_number()
            comments = self.video_comments()
            video_thumbnail = self.video_thumbnail(link)
            download_link = self.video_downloader(link)

            dt = {"Name": self.Name, "Channel Id": self.channel_id, "Title": title, "Likes": likes,
                  "Comments Number": comments_number, "Video Views": video_view,
                  "Video Link": link, "Thumbnail": video_thumbnail, "Download Link": download_link}
            # print("Total links found:", len(list_of_links))
            # print("All th links are", list_of_links)
            # print(dt)
            # print("Comments details are", comments)
            return dt, comments

        except Exception:
            print("Please check the name again and retry or check internet connection")


if __name__ == '__main__':
    # pass
    try:
        obj1 = Youtube()
    except Exception:
        print("Please check the name again and retry")

    # obj1.execute_browser(obj1.channel_videos())
    # obj1.scroll_me(value_down=1500)
    # time.sleep(2)
    # obj1.scroll_me(value_down=1500)
    # time.sleep(2)
    # print(len(obj1.channel_videos_link()))
    # obj1.video_comments()
    # obj1.video_likes()
    # obj1.video_comment_views_number()
    # obj1.video_thumbnail()
    # obj1.video_title()
    # obj1.video_downloader()
    # obj1.extract_everything_from_video()
