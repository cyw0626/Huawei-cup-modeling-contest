def zuiyou(bingo,centroids):
    min1=0

    best1=np.zeros((len(bingo),1))
    for i in range (len(bingo)):
        a=centroids[0][1]-hanshu1(bingo[i])

        b=centroids[1][1]-hanshu2(bingo[i])

        c=centroids[2][1]-hanshu3(bingo[i])

        d=(0.5*a+0.3*b+0.2*c)
        if (d=min(d,min1)):
            min1=d
            e=bingo[i]
            print ('最优解＝',bingo[i])

    return e
pbest=zuiyou(bingo,centroids)
plt.plot(range(0,1300),pbest)
plt.show()    