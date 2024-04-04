import os
import csv
import googleapiclient.discovery

def run_airflow_etl():

    def write_data_to_csv(comments_list):
        # Specify the CSV file name
        csv_file = 'output.csv'

        # Specify the field names
        fields = ['author', 'comment', 'published_at']
        # Writing to CSV file
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            # Create a CSV writer object
            csv_writer = csv.DictWriter(csvfile, fieldnames=fields)

            # Write the header
            csv_writer.writeheader()

            # Write the data
            csv_writer.writerows(comments_list)
        print(f'Data has been written to {csv_file}')

    def process_comments(response_items):
        comments = []
        for comment in response_items:
                author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
                comment_text = comment['snippet']['topLevelComment']['snippet']['textOriginal']
                publish_time = comment['snippet']['topLevelComment']['snippet']['publishedAt']
                comment_info = {'author': author, 
                        'comment': comment_text, 'published_at': publish_time}
                comments.append(comment_info)
        print(f'Finished processing {len(comments)} comments.')
        return comments

    def main():

        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyBcFpMeATiA66ET8khDy40ry_6fPhxy3Nc"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = DEVELOPER_KEY)
        request = youtube.commentThreads().list(
            part="snippet, replies",
            videoId="q8q3OFFfY6c"
        )
        response = request.execute()
        
        comments_list = []
        while response.get('nextPageToken', None):
            request = youtube.commentThreads().list(
                part='replies,snippet',
                videoId="q8q3OFFfY6c",
                pageToken=response['nextPageToken']
            )
            response = request.execute()
            comments_list.extend(process_comments(response['items']))
        print(comments_list)

        write_data_to_csv(comments_list)
    if __name__ == "__main__":
        main()