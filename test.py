import pickle
import gcVisual
# Load the action history file
file_path = "C:/Users/LEE/Downloads/action_history_09_13_102319.pkl"

with open(file_path, 'rb') as f:
    data = pickle.load(f)
print(data.keys())
print(data[0])
#app = gcVisual.start_gui()
#gcVisual.update_states(app, stateList1, stateList2)
#app.mainloop()