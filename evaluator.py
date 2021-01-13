class Evaluator:

    def __init__(self, result):
        "takes path of result to evaluate"
        self.times = []
        self.shape = []
        self.color = []
        # se změnou tématu otázek
        self.with_fault = []
        self.without_fault = []
        # se změnou otázek
        self.with_task_change_with_switch = []
        # beze změny otázky
        self.without_task_change = []
        # se změnou otázek pokud se neměnilo téma
        self.with_task_change_without_switch = []

        self.last = "X"
        self.last_task = "X"

        self.evaluate(result)
        self.approximate()
        if True:
            self.save(result)

    def evaluate(self, result):
        f = open("results/results"+result+".txt", "r")
        f.readline()

        for line in f:
            # mine line
            line = line.split('_')
            time = float(line[0])
            success = int(line[1])
            task = int(line[2])

            if time -2 > 0:
                print(time-2)
                print("last theme:", self.last)
                print("last task:", self.last_task)
                # if is time valid
                self.times.append(time-2)

                if task >= 2:
                    self.color.append(time-2)
                    actual = True
                else:
                    self.shape.append(time-2)
                    actual = False
                print("actual theme:", actual)
                print("actual task:", task)
                if success:
                    # 0 znamená, zápor pro neúspěch... z pohledu odsud to je blbost, z pohledu Guy.py to smysl dává
                    self.with_fault.append(time-2)
                else:
                    self.without_fault.append(time-2)

                if self.last != "X":
                    if self.last_task != task:
                        print("změna úkolu")
                        print(self.last)
                        # poslední úkol není stejný
                        if self.last == actual:
                            print("stejné téme")
                            # poslední téma je stejné
                            self.with_task_change_without_switch.append(time-2)
                        else:
                            print("změna tématu")
                            # poslední téma bylo jiné
                            self.with_task_change_with_switch.append(time-2)
                    else:
                        print("stejný úkol")
                        # poslední úkol byl stejný
                        self.without_task_change.append(time-2)

                self.last_task = task
                self.last = actual
                print()
                print()
                print()

    def approximate(self):
        self.apx_time = self.get_mean(self.times)
        self.apx_color_time = self.get_mean(self.color)
        self.apx_shape_time = self.get_mean(self.shape)
        self.apx_time_w_falut = self.get_mean(self.with_fault)
        self.apx_time_n_fault = self.get_mean(self.without_fault)
        self.apx_time_w_change_w_switch = self.get_mean(self.with_task_change_with_switch)
        self.apx_time_w_change_n_switch = self.get_mean(self.with_task_change_without_switch)
        self.apx_time_n_change = self.get_mean(self.without_task_change)

    def get_mean(self, array):
        count = sum(array)
        try:
            return count/len(array)
        except:
            return "none"

    def get_difference(self, time):
        if time != "none":
            res = self.apx_time - time
            if res < 0.0:
                return "+" + str(abs(res))
            elif res == 0:
                return 0
            else:
                return "-" + str(res)
        return time

    def print(self):
        print("průměrný čas:", self.apx_time)
        print("otázka na barvu:", self.apx_color_time)
        print("otázka na tvar:", self.apx_shape_time)
        print("čas chybné odpovědi:", self.apx_time_w_falut)
        print("čas správné odpovědi:", self.apx_time_n_fault)
        print("změna otázky beze změny kategorie:", self.apx_time_w_change_n_switch)
        print("změna otázky se změnou kategorie:", self.apx_time_w_change_w_switch)
        print("beze změny otázky:", self.apx_time_n_change)

    def save(self, result):
        self.f = open("evaluations/evaluation"+result+".txt", "w")
        self.save_averages()
        self.save_differences()
        self.save_deviations()
        self.save_times()

    def write(self, array):
        i = 1
        for time in array:
            if i < 10:
                self.f.write("\n" + str(i)+"______" + str(time))
            else:
                self.f.write("\n" + str(i)+"_____" + str(time))
            i +=1
        self.f.write("\n")

    def get_deviation_from_mean(self, array):

        mean = self.get_mean(array)
        top = max(array)
        low = min(array)

        devs = [top-mean, mean-low]
        minimal_deviation_from_mean = min(devs)
        maximal_deviation_from_mean = max(devs)
        average_deviation = self.get_mean(devs)

        return minimal_deviation_from_mean, maximal_deviation_from_mean, average_deviation

    def write_deviations(self, array):
        if array:
            devs = self.get_deviation_from_mean(array)
            self.f.write("\n   minimal deviation: " + str(devs[0]))
            self.f.write("\n   maximal deviation: " + str(devs[1]))
            self.f.write("\n   average deviation: " + str(devs[2]))
        else:
            self.f.write("\n   none")

    def save_averages(self):
        self.f.write("average time: " + str(self.apx_time))
        self.f.write("\ncolor task: " + str(self.apx_color_time))
        self.f.write("\nshape task: " + str(self.apx_shape_time))
        self.f.write("\naverage time of wrong answer: " + str(self.apx_time_w_falut))
        self.f.write("\naverage time of correct answer: " + str(self.apx_time_n_fault))
        self.f.write("\nchange of task without change of category: " + str(self.apx_time_w_change_n_switch))
        self.f.write("\nchange of task with change of category: " + str(self.apx_time_w_change_w_switch))
        self.f.write("\nwith same task: " + str(self.apx_time_n_change))

    def save_differences(self):
        self.f.write("\n\naverage time: " + str(self.get_difference(self.apx_time)))
        self.f.write("\ncolor task: " + str(self.get_difference(self.apx_color_time)))
        self.f.write("\nshape task: " + str(self.get_difference(self.apx_shape_time)))
        self.f.write("\naverage time of wrong answer: " + str(self.get_difference(self.apx_time_w_falut)))
        self.f.write("\naverage time of correct answer: " + str(self.get_difference(self.apx_time_n_fault)))
        self.f.write("\nchange of task without change of category: " + str(self.get_difference(self.apx_time_w_change_n_switch)))
        self.f.write("\nchange of task with change of category: " + str(self.get_difference(self.apx_time_w_change_w_switch)))
        self.f.write("\nwith same task: " + str(self.get_difference(self.apx_time_n_change)))

    def save_deviations(self):
        self.f.write("\n\ndeviations: ")
        self.write_deviations(self.times)
        self.f.write("\ncolor task deviations: ")
        self.write_deviations(self.color)
        self.f.write("\nshape task deviations: ")
        self.write_deviations(self.shape)
        self.f.write("\naverage time of wrong answer deviations: ")
        self.write_deviations(self.with_fault)
        self.f.write("\naverage time of correct answer deviations: ")
        self.write_deviations(self.without_fault)
        self.f.write("\nchange of task without change of category deviations: ")
        self.write_deviations(self.with_task_change_without_switch)
        self.f.write("\nchange of task with change of category deviations: ")
        self.write_deviations(self.with_task_change_with_switch)
        self.f.write("\nwith same task deviations: ")
        self.write_deviations(self.without_task_change)

    def save_times(self):
        self.f.write("\n\ntask times: ")
        self.f.write("\n\ncolor task times: ")
        self.write(self.color)
        self.f.write("\nshape task times: ")
        self.write(self.shape)
        self.f.write("\naverage times of wrong answer: ")
        self.write(self.with_fault)
        self.f.write("\naverage times of correct answer: ")
        self.write(self.without_fault)
        self.f.write("\nchange of task without change of category times: ")
        self.write(self.with_task_change_without_switch)
        self.f.write("\nchange of task with change of category times: ")
        self.write(self.with_task_change_with_switch)
        self.f.write("\nwith same task times: ")
        self.write(self.without_task_change)
