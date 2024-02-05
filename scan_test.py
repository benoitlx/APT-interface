from apt_interface.scan import Scan
import matplotlib.pyplot as plt


def main():
    s = Scan((None))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = [i for i, j, k in s.coords]
    y = [j for i, j, k in s.coords]
    z = [k for i, j, k in s.coords]
    ax.plot3D(x, y, z)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

if __name__ == "__main__":
    main()
