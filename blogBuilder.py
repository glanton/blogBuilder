import csv
import xml.etree.ElementTree as ET


# initialize blog data with headers as first element
blog_data = [["Title", "Body", "Path", "Created Date", "Categories", "Files"]]

# build the xml tree
tree = ET.parse("wp_export.xml")
root = tree.getroot()

# find and iterate over every <item> element
line_count = 1
items = root.iter("item")
for item in items:

    # find text of row fields and surround body in <p> tags
    title = item.find("title").text
    body = item.find("{http://purl.org/rss/1.0/modules/content/}encoded").text
    body = "<p>" + str(body) + "</p>"
    path = item.find("{http://wordpress.org/export/1.2/}post_name").text
    created_date = item.find("{http://wordpress.org/export/1.2/}post_date").text

    # debug log
    print(str(line_count) + " " + title)
    line_count += 1

    # find and format any taxonomy tags
    tags = ""
    categories = item.findall("category")
    for category in categories:
        if "domain" in category.attrib:
            if category.attrib["domain"] == "category":
                tags += category.text + "|"

    # find text of extra meta data
    comment_status = item.find("{http://wordpress.org/export/1.2/}comment_status").text
    post_type = item.find("{http://wordpress.org/export/1.2/}post_type").text
    status = item.find("{http://wordpress.org/export/1.2/}status").text

    # set files to empty
    files = ""

    # only build list of post type is post (not page)
    if post_type == "post" and status == "publish":

        # build list of post from data and append post to blog data
        post = [title, body, path, created_date, tags, files]
        blog_data.append(post)

# save blog data to csv file
with open("blog_data.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(blog_data)
