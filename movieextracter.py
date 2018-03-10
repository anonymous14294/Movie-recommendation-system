import sqlite3

conn = sqlite3.connect('movielens.sqlite')
cur = conn.cursor()
genre = input('Enter the category of movie: ')
genre = '%' + genre + '%'
tag = input('Enter the tag : ')
tag = '%' + tag + '%'
movie = {}

# this function calculate ratings of a movie by all users and returns average rating
def rating_chker(mid):
    rating_list = []
    cur.execute('SELECT ratings FROM Ratings WHERE m_id = ?', (mid,))
    row = cur.fetchall()
    for line in row:
        rating = line[0]
        rating_list.append(rating)
    # if movie is not rated by any user
    try:
        add = sum(rating_list)
        avg_rating = add/len(rating_list)
        return avg_rating
    except ZeroDivisionError:
        return None

# it returns ctegory of movie
def category_chkr(mid):
    cur.execute('SELECT category_id FROM Movies WHERE m_id = ?',(mid, ))
    row = cur.fetchone()[0]
    cur.execute('SELECT category FROM Category WHERE id = ?', (row, ))
    category = cur.fetchone()[0]

    return category

# it returns tag of movie if any
def tag_chkr(mid):
    cur.execute('SELECT tag_id FROM Tags WHERE m_id = ?', (mid, ))
    try:
        row = cur.fetchone()[0]
        cur.execute('SELECT tag FROM Tag WHERE id = ?', (row, ))
        tag = cur.fetchone()[0]
        return tag
    except:
        return None

cur.execute('SELECT id FROM Category WHERE category LIKE ? ', (genre, ))
row = cur.fetchall()
if len(row) < 1:
    print('invalid category')
    print('Now Searching according to Tags.....')
else:
    for line in row:
        catg = line[0]
        cur.execute('SELECT m_id, m_name FROM Movies WHERE category_id = ?', (catg, ))
        films = cur.fetchall()
        for lst in films:
            ids = lst[0]
            name = lst[1]
            movie[name] = ids

if len(tag) > 1:
    cur.execute('SELECT id FROM Tag WHERE tag LIKE ? ', (tag, ))
    row = cur.fetchall()
    if len(row) < 1:
        print('Could not find the tag')
    else:
        for line in row:
            ids = line[0]
            cur.execute('SELECT m_id FROM Tags WHERE tag_id = ?', (ids, ))
            films = cur.fetchall()
            for lst in films:
                mid = lst[0]
                if mid not in movie.values():
                    cur.execute('SELECT m_name FROM Movies WHERE m_id = ?', (mid,))
                    new_film = cur.fetchone()[0]
                    movie[new_film] = mid
                else:
                    continue
else:
    print("Wrong Tag")
if len(movie) < 1:
    print('Movies not found ')
else:
    print('According to filters ur movies are ')
    try:
        for key, value in movie.items():
            rating = rating_chker(value)
            category = category_chkr(value)
            tags = tag_chkr(value)
            try:
                print('Movie: ', key, 'Avarage user Rating: {0:.2f}'.format(rating), 'Category: ', category, "Tag: ", tags)
            except:
                print('Movie: ', key, 'Movie is not rated by any user', 'Category: ', category, "Tag: ", tags)
    except KeyboardInterrupt:
        print('===========================')
        print('Program intreupted by user')
