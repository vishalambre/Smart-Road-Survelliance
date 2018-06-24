import matplotlib.pyplot as plt

def graph():
    thresh = 15
    x1 = [1, 3, 5, 7, 9]
    y1 = [25, 17, 9, 9, 7]

    plt.axhline(thresh,color='k',linewidth=3)

    plt.bar(x1, y1, color='r')
    for (val,val2) in zip(x1,y1):
        if val2 < thresh:
            plt.bar(val, val2 , color='b')
        else:
            plt.bar(val, thresh, color = 'b')

    plt.xlabel('Vehicles')
    plt.ylabel('Speed')
    plt.xticks(x1,['ID1','ID2','ID3','ID4','ID5'])
    plt.legend()
    plt.title('Speed Detection')

    plt.show()

if __name__ == '__main__':
    graph()
