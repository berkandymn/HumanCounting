import math
from influxdb import InfluxDBClient
dizi=[]

def ilkDeger():
    # InfluxDB'ye bağlanma
    client = InfluxDBClient(host='192.168.0.11', port=8086, username='', password='', database='insidePeople')

    # Son veriyi sorgulama
    result = client.query('SELECT last(value)  FROM people')

    points = result.get_points()

    # İlk satırı al ve 'last' değerini al
    for point in points:
        last_value = point['last']
    return int(last_value)

ppl=ilkDeger()

class EuclideanDistTracker:
    def __init__(self):
        self.center_points = {}
        self.yuk = 0
        self.gen = 0
        self.ppl=ppl
        self.id_count = 0

    def frame(self,width,height):
        self.yuk=width
        self.gen=height
    def update(self, objects_rect):
        for rect in objects_rect:
            x, y = rect
            if self.yuk<y<self.gen:
                same_object_detected = False
                for id, pt in self.center_points.items():
                    #öklid uzaklık değerinin hesaplanması
                    dist = math.hypot(x - pt[-1][0], y - pt[-1][1])

                    #öklid uzaklık değer karşılaştırma
                    if dist < 25:
                        self.center_points[id].append((x, y))
                        same_object_detected = True
                        break
                if same_object_detected is False:
                    self.center_points[self.id_count] = [(x, y)]
                    self.id_count += 1
            else:
                for k, at in self.center_points.items():
                    if at[-1][1] + at[0][1] > self.yuk + self.gen - 15:
                        if at[0][1] - at[-1][1] < 0 and len(at)>10:
                            self.ppl += 1
                            self.center_points[k]=[(0,0)]
                        elif at[0][1] - at[-1][1] > 0 and len(at)>10:
                            self.ppl -= 1
                            self.center_points[k]=[(0,0)]
        return self.ppl