import matplotlib.pyplot as plt
import numpy as np
import myconfig


# General functions
def plot_loss_curve(
        title: str, x: int, y: int, y_test: int, ylim: float = 0.6, path: str = '') -> None:
    plt.figure()
    plt.title(title)
    axes = plt.gca()
    axes.set_ylim([0, ylim])
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    train_sizes = x
    train_scores = y
    test_scores = y_test

    plt.grid()

    plt.plot(
        train_sizes,
        train_scores,
        "o-",
        label="Training Loss",
    )
    plt.plot(
        train_sizes,
        test_scores,
        "o-",
        label="Validation Loss",
    )

    plt.legend(loc="best")

    plt.savefig(path + 'train_loss.png', bbox_inches='tight')


def plot_accuracy_curve(
        title: str, x: int, y: int, y_test: int, ylim: float = 0.6, path: str = '') -> None:
    plt.figure()
    plt.title(title)
    axes = plt.gca()
    axes.set_ylim([ylim, 1])
    plt.xlabel("Epoch")
    plt.ylabel("accuracy")
    train_sizes = x
    train_scores = y
    test_scores = y_test

    plt.grid()

    plt.plot(
        train_sizes,
        train_scores,
        "o-",
        label="Training accuracy",
    )
    plt.plot(
        train_sizes,
        test_scores,
        "o-",
        label="Validation accuracy",
    )

    plt.legend(loc="best")

    plt.savefig(path + 'train_accuracy.png', bbox_inches='tight')


result_dir = myconfig.savepath
log_path = result_dir + 'training_log.csv'
save_path = result_dir
log_file = open(log_path, 'r')
logs = log_file.readlines()
log_file.close()

train_loss = []
train_accuracy = []
valid_loss = []
valid_accuracy = []

# print(len(logs))
for i in range(1, len(logs)):
    temp = logs[i].split(';', -1)
    train_accuracy.append(float(temp[1]))
    train_loss.append(float(temp[2]))
    valid_accuracy.append(float(temp[-2]))
    valid_loss.append(float(temp[-1][:-1]))

# print(len(train_accuracy))

plot_loss_curve("Training process", np.arange(1, 1 + len(train_loss)), train_loss, valid_loss, max(valid_loss), save_path)
plot_accuracy_curve("Training process", np.arange(1, 1 + len(train_accuracy)), train_accuracy, valid_accuracy, 0,
                    save_path)
