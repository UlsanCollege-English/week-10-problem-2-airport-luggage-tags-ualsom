"""
HW02 — Airport Luggage Tags (Open Addressing with Delete)
Implement linear probing with EMPTY and DELETED markers.
"""

# Step 4: create unique marker objects
EMPTY = object()
DELETED = object()

def make_table_open(m):
    """Return a table of length m filled with EMPTY markers."""
    return [EMPTY] * m

def _hash_basic(s):
    """Simple hash: sum of character ordinals."""
    return sum(ord(c) for c in s)

def _find_slot_for_insert(t, key):
    """Return index to insert/overwrite (may return DELETED slot). Return None if full."""
    m = len(t)
    first_deleted = None
    start = _hash_basic(key) % m

    for i in range(m):
        idx = (start + i) % m
        slot = t[idx]

        # Empty → can insert
        if slot is EMPTY:
            return first_deleted if first_deleted is not None else idx
        # Deleted → remember first deleted
        elif slot is DELETED:
            if first_deleted is None:
                first_deleted = idx
        # Same key → overwrite
        elif slot[0] == key:
            return idx
    return first_deleted  # None if full and no deleted slot

def _find_slot_for_search(t, key):
    """Return index where key is found; else None. DELETED does not stop search."""
    m = len(t)
    start = _hash_basic(key) % m

    for i in range(m):
        idx = (start + i) % m
        slot = t[idx]

        if slot is EMPTY:
            # stop at first EMPTY (key not present)
            return None
        elif slot is DELETED:
            # skip deleted
            continue
        elif slot[0] == key:
            return idx
    return None

def put_open(t, key, value):
    """Insert or overwrite (key, value). Return True on success, False if table is full."""
    idx = _find_slot_for_insert(t, key)
    if idx is None:
        return False  # table full

    t[idx] = (key, value)
    return True

def get_open(t, key):
    """Return value for key or None if not present."""
    idx = _find_slot_for_search(t, key)
    if idx is None:
        return None
    return t[idx][1]

def delete_open(t, key):
    """Delete key if present. Return True if removed, else False."""
    idx = _find_slot_for_search(t, key)
    if idx is None:
        return False
    t[idx] = DELETED
    return True

if __name__ == "__main__":
    # Optional manual checks (not graded)
    table = make_table_open(5)
    put_open(table, "A1", "Apple")
    put_open(table, "B2", "Banana")
    put_open(table, "C3", "Cherry")
    print(get_open(table, "B2"))     # Banana
    delete_open(table, "B2")
    print(get_open(table, "B2"))     # None
    print(table)
