class ParetoFront(dict):
    def __setitem__(self, A, As):
        dominated = set()

        for B, Bs in self.items():
            if (
                all(b >= a for a, b in zip(As, Bs, strict=True))
                and any(b > a for a, b in zip(As, Bs, strict=True))
            ):
                return

            if (
                all(a >= b for a, b in zip(As, Bs, strict=True))
                and any(a > b for a, b in zip(As, Bs, strict=True))
            ):
                dominated.add(B)

        for B in dominated:
            super().__delitem__(B)

        super().__setitem__(A, As)
