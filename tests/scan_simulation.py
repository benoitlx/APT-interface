from apt_interface.scan import Scan
import matplotlib.pyplot as plt


def main():
    s = Scan((None))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = [i for i, j in s.coords]
    y = [j for i, j in s.coords]
    # z = [k for i, j in s.coords]
    ax.plot(x, y) 

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

if __name__ == "__main__":
    main()
