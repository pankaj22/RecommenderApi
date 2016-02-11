import math

def get_polarity(reviews):
    polarity=[]
    for i in range(0,len(reviews)):
        polarity.append(reviews[i]['polarity'])

    return polarity

def mapping(polarity,weight):
    sz = len(polarity)
    polarity = sorted(polarity, reverse=True)
    d = {}
    for i in range(0,sz):
        d[polarity[i]]=weight
        weight -= 1
    return d

def calculate_rating(positive_reviews,negative_reviews):
    pos_sz = len(positive_reviews)
    neg_sz = len(negative_reviews)

    if pos_sz==1 and neg_sz==0:
        rating = 5 + (positive_reviews[0]['polarity'])/20
        return rating
    if neg_sz==1 and pos_sz==0:
        rating = 5 - (negative_reviews[0]['polarity'])/20
        return rating

    positive_polarity = get_polarity(positive_reviews)
    negative_polarity = get_polarity(negative_reviews)

    unique_pos = list(set(positive_polarity))
    unique_neg = list(set(negative_polarity))
    pos_weight = mapping(unique_pos,pos_sz)
    neg_weight = mapping(unique_neg,neg_sz)

    num = deno =0
    if pos_sz>0:
        for i in range(0,pos_sz):
            p = positive_reviews[i]['polarity']
            num += (p*pos_weight[p])
            deno += p
        pos_fac = float(num)/deno
        pos_scale = 5.0*(float(pos_fac)/pos_sz)
    else:
        pos_scale=0

    num = deno = 0
    if neg_sz>0:
        for i in range(0,neg_sz):
            p = negative_reviews[i]['polarity']
            num += (p*neg_weight[p])
            deno += p
        neg_fac = float(num)/deno
        neg_scale = 5.0*(float(neg_fac)/neg_sz)
    else:
        neg_scale=0

    portion=5
    if(pos_sz>neg_sz):
        if neg_sz>0:
            portion = float(pos_sz)/neg_sz
        rating = 5 + pos_scale - (neg_scale/portion)
    elif(pos_sz<neg_sz):
        if pos_sz>0:
            portion = float(neg_sz)/pos_sz
        rating = 5 + (pos_scale/portion) - neg_scale
    else:
        rating = 5 + pos_scale - neg_scale

    return rating
