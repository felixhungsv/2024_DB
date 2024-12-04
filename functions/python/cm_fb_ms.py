import utils

def message(user):
    columns, data = utils.query(f'''
    SELECT 
        CASE 
            WHEN u_s.username = '{user}' THEN u_r.username
            ELSE u_s.username
        END AS the_username,
        MAX(m.mgtime) AS last_message_time
    FROM MESSAGE AS m
    JOIN USERS AS u_s ON m.senderid = u_s.userid
    JOIN USERS AS u_r ON m.receiverid = u_r.userid
    WHERE u_s.username = '{user}' OR u_r.username = '{user}'
    GROUP BY the_username
    ORDER BY last_message_time DESC
    limit 10
    ''') 
    return utils.pd.DataFrame(data, columns=columns)

def message_people(user, other_user):
    columns, data = utils.query(f'''
    SELECT m.senderid, u_s.username as senderName, m.receiverid, u_r.username as receiverName, m.mgtime, mgcontent
    from MESSAGE as m
    join USERS as u_s on m.senderid = u_s.userid
    join USERS as u_r on m.receiverid = u_r.userid
    where (senderName = '{user}' and receiverName = '{other_user}') or (senderName = '{other_user}' and receiverName = '{user}')
    order by mgtime desc
            ''') 
    return utils.pd.DataFrame(data, columns=columns)

def feedback():
    columns, data = utils.query('''
    SELECT f.userid, u.username, f.fbtime, f.fbcontent
    from feedback as f
    join USERS as u on f.userid = u.userid
    ''')
    return utils.pd.DataFrame(data, columns=columns).sort_values("fbtime")

def comment(itemID):
    columns, data = utils.query(f'''
    SELECT c.memberid, u.username, c.itemid, i.description, c.cmtime, c.cmcontent
    from COMMENTS as c
    join USERS as u on c.memberid = u.userid
    join ITEM as i on c.itemid = i.itemid
    WHERE i.itemid = '{itemID}'
    ''')
    # 將結果轉換為 DataFrame
    return utils.pd.DataFrame(data, columns=columns).sort_values("cmtime")

