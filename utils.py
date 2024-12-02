class Time:
    """時刻を表すクラス"""
    def __init__(self, hours, minutes):
        self.hours = hours
        self.minutes = minutes

    def add_time(self, minutes):
        """時刻の加算"""
        total_minutes = self.minutes + minutes
        self.hours += total_minutes // 60
        self.minutes = total_minutes % 60


class Process:
    """工程データを表すクラス"""
    def __init__(self, event, information, nkm, nup, ndown, duration):
        self.event = event
        self.information = information
        self.nkm = int(nkm) if nkm.isdigit() or nkm.lstrip('-').isdigit() else -1
        self.nup = int(nup) if nup.isdigit() or nup.lstrip('-').isdigit() else -1
        self.ndown = int(ndown) if ndown.isdigit() or ndown.lstrip('-').isdigit() else -1
        self.duration = int(duration) if duration.isdigit() else 0


def process_group_data(groups):
    """
    C言語の形式に準拠したスケジュール計算を行い、結果を文字列で返す。
    """
    start_time = Time(6, 0)  # 開始時刻
    processes = [Process(*group) for group in groups]
    current_time = start_time

    result = ""  # 出力結果を保持する文字列
    total_distance, total_up, total_down = 0, 0, 0

    # 各工程の距離アップダウンを合計
    for process in processes:
        if process.nkm > 0:
            total_distance += process.nkm
        if process.nup > 0:
            total_up += process.nup
        if process.ndown > 0:
            total_down += process.ndown

    result += f"{total_distance}km {total_up}up {total_down}down\n\n"

    for i, process in enumerate(processes):
        # 現在の時刻とイベント名
        result += f"{current_time.hours:02d}:{current_time.minutes:02d} {process.event}\n"

        if i == len(processes) - 1:  # 最後の工程の場合
            break

        # ↓ 情報
        duration_str = ""
        if process.duration > 0:
            if process.duration % 60 == 0:
                duration_str = f"{process.duration // 60}h"
            elif process.duration % 60 == 30:
                duration_str = f"{process.duration // 60}.5h"
            else:
                duration_str = f"{process.duration}min"

        movement = []
        if process.nkm == -1:
            movement.append("微km")
        elif process.nkm > 0:
            movement.append(f"{process.nkm}km")

        if process.nup == -1:
            movement.append("微up")
        elif process.nup > 0:
            movement.append(f"{process.nup}up")

        if process.ndown == -1:
            movement.append("微down")
        elif process.ndown > 0:
            movement.append(f"{process.ndown}down")

        result += f"\n↓{process.information} {' '.join(movement)} {duration_str}\n"

        # 次の時刻を計算
        current_time.add_time(process.duration)

    return result
