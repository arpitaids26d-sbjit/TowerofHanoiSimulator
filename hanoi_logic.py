# hanoi_logic.py
# Is file mein Tower of Hanoi ka logic hai (recursion ke saath)

def minimum_moves(n):
    """Minimum moves = 2^n - 1"""
    return (2 ** n) - 1


def solve_hanoi(n, source, auxiliary, destination, moves):
    """
    Recursion se Tower of Hanoi solve karta hai.
    Har move (from_rod, to_rod) ki tarah 'moves' list mein save hota hai.
    """
    # Base case: agar koi disk nahi hai, to kuch nahi karna
    if n == 0:
        return

    # Step 1: Upar ke (n-1) disks ko source se auxiliary par bhejo
    solve_hanoi(n - 1, source, destination, auxiliary, moves)

    # Step 2: Sabse bada disk source se destination par bhejo
    moves.append((source, destination))

    # Step 3: (n-1) disks ko auxiliary se destination par bhejo
    solve_hanoi(n - 1, auxiliary, source, destination, moves)


def get_all_moves(n):
    """n disks ke saare moves ki list return karta hai.
    Rods ke naam: 0 = Source, 1 = Auxiliary, 2 = Destination"""
    moves = []
    solve_hanoi(n, 0, 1, 2, moves)
    return moves