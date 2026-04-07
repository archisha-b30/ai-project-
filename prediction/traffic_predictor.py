import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class LSTMPredictor(nn.Module):
    def __init__(self, input_size=1, hidden_size=50, num_layers=1, output_size=5):
        super(LSTMPredictor, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

class TrafficPredictor:
    """
    Predicts future traffic using LSTM.
    Input: historical total vehicle counts
    Output: predicted counts for next steps
    """

    def __init__(self, seq_length=10, predict_steps=5):
        self.seq_length = seq_length
        self.predict_steps = predict_steps
        self.model = LSTMPredictor(output_size=predict_steps)
        self.scaler = MinMaxScaler()
        self.trained = False
        self.data_min = None
        self.data_max = None

    def prepare_data(self, data):
        # data: list of total counts
        if len(data) < self.seq_length + 1:
            return None, None
        
        data = np.array(data).reshape(-1, 1).astype(np.float32)
        scaled = self.scaler.fit_transform(data)
        X, y = [], []
        
        for i in range(len(scaled) - self.seq_length - self.predict_steps + 1):
            X.append(scaled[i:i+self.seq_length])
            y.append(scaled[i+self.seq_length:i+self.seq_length+self.predict_steps].flatten())
        
        if len(X) == 0:
            return None, None
            
        return np.array(X), np.array(y)

    def train(self, data, epochs=50):
        try:
            X, y = self.prepare_data(data)
            if X is None or len(X) == 0:
                self.trained = False
                return
            
            X = torch.tensor(X, dtype=torch.float32)
            y = torch.tensor(y, dtype=torch.float32)
            
            criterion = nn.MSELoss()
            optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)
            
            for epoch in range(epochs):
                outputs = self.model(X)
                loss = criterion(outputs, y)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            
            self.trained = True
        except Exception as e:
            print(f"Training error: {e}")
            self.trained = False

    def predict(self, history):
        try:
            if not self.trained or len(history) < self.seq_length:
                # Return moving average if not enough history
                if len(history) > 0:
                    avg = float(np.mean(history[-min(5, len(history)):]))
                    return [avg] * self.predict_steps
                return [0.0] * self.predict_steps
            
            # Use last seq_length values
            recent = np.array(history[-self.seq_length:]).reshape(-1, 1).astype(np.float32)
            scaled = self.scaler.transform(recent)
            X = torch.tensor(scaled.reshape(1, self.seq_length, 1), dtype=torch.float32)
            
            with torch.no_grad():
                pred = self.model(X).numpy().flatten()
            
            # Inverse transform to get original scale
            pred = self.scaler.inverse_transform(pred.reshape(-1, 1)).flatten()
            return [float(p) for p in pred]
        except Exception as e:
            print(f"Prediction error: {e}")
            return [float(np.mean(history[-5:])) if len(history) > 0 else 0.0] * self.predict_steps