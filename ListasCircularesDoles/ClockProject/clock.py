import math

def draw_clock(canvas, now):
    width = int(canvas['width'])
    height = int(canvas['height'])
    center_x = width // 2
    center_y = height // 2
    radius = min(center_x, center_y) - 10

    canvas.create_oval(center_x - radius, center_y - radius,
                       center_x + radius, center_y + radius,
                       fill="#ffe6f0", outline="black")

    # Números del reloj
    for i in range(1, 13):
        angle = math.pi/6 * (i - 3)
        x = center_x + math.cos(angle) * (radius - 20)
        y = center_y + math.sin(angle) * (radius - 20)
        canvas.create_text(x, y, text=str(i), font=("Helvetica", 12, "bold"))

    # Líneas de minutos
    for i in range(60):
        angle = math.radians(i * 6)
        x_start = center_x + math.cos(angle) * (radius - 5)
        y_start = center_y + math.sin(angle) * (radius - 5)
        x_end = center_x + math.cos(angle) * (radius - 1)
        y_end = center_y + math.sin(angle) * (radius - 1)
        canvas.create_line(x_start, y_start, x_end, y_end, fill="black")

    hour = now.hour % 12
    minute = now.minute
    second = now.second

    hour_angle = math.radians((hour + minute / 60) * 30 - 90)
    minute_angle = math.radians(minute * 6 - 90)
    second_angle = math.radians(second * 6 - 90)

    hour_length = radius * 0.5
    minute_length = radius * 0.8
    second_length = radius * 0.9

    canvas.create_line(center_x, center_y,
                       center_x + hour_length * math.cos(hour_angle),
                       center_y + hour_length * math.sin(hour_angle),
                       width=6, fill="#8b008b")

    canvas.create_line(center_x, center_y,
                       center_x + minute_length * math.cos(minute_angle),
                       center_y + minute_length * math.sin(minute_angle),
                       width=4, fill="#c71585")

    canvas.create_line(center_x, center_y,
                       center_x + second_length * math.cos(second_angle),
                       center_y + second_length * math.sin(second_angle),
                       width=2, fill="red")
