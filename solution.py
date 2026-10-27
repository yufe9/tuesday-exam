# 강의실 예약 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

ROOMS = ("A101", "A102", "B201")
DAYS = ("월", "화", "수", "목", "금")
OPEN, CLOSE, MAX_LEN, MAX_PER_DAY = 9, 21, 3, 2


def _is_int(v):
    # bool 은 int 의 하위 클래스라 type 으로 정확히 비교해야 걸러짐
    return type(v) is int


def _valid_place(room, day):
    # 리스트 같은 값이 들어와도 예외 없이 False 가 되도록 튜플 비교만 사용
    return room in ROOMS and day in DAYS


class RoomBooking:
    def __init__(self):
        # (room, day) → [(start, end, name), ...]
        self._data = {}

    def book(self, room, day, start, end, name):
        if not isinstance(name, str) or not name.strip():   # 빈 이름·공백·None 거절
            return False
        if not _valid_place(room, day):
            return False
        if not (_is_int(start) and _is_int(end)):
            return False
        if start < OPEN or end > CLOSE or start >= end or end - start > MAX_LEN:
            return False
        slots = self._data.get((room, day), [])
        if any(start < e and s < end for s, e, _ in slots):
            return False
        count = sum(1 for (_, d), lst in self._data.items() if d == day
                    for _, _, n in lst if n == name)
        if count >= MAX_PER_DAY:
            return False
        self._data.setdefault((room, day), []).append((start, end, name))
        return True

    def cancel(self, room, day, start, name):
        if not _valid_place(room, day) or not _is_int(start):
            return False
        slots = self._data.get((room, day), [])
        for i, (s, _, n) in enumerate(slots):
            if s == start:
                if n != name:
                    return False
                del slots[i]
                return True
        return False

    def get_schedule(self, room, day):
        if not _valid_place(room, day):
            return []
        return sorted(self._data.get((room, day), []))
