#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""

"""
from trackplot.base.GenomicLoci import GenomicLoci


class Stroke(object):
    __slots__ = ["start", "end", "color", "label", "origin"]

    def __init__(self, start: int, end: int, color: str = "red", label: str = "", origin: str = ""):
        self.start = start
        self.end = end
        self.color = color
        self.label = label
        self.origin = origin if origin else f"{start}-{end}@{color}-{label}"

    def __str__(self):
        return self.origin

    @property
    def center(self) -> float:
        return (self.end + self.start) / 2

    @classmethod
    def create(cls, stroke: str, region: GenomicLoci, default_color: str = "red"):
        res = []
        for i in stroke.split(":"):
            i = i.split("@")
            sites = sorted([int(x) - region.start for x in i[0].split("-")])
            if sites[0] < 0:
                sites[0] = 0

            if sites[-1] > len(region):
                sites[-1] = len(region)

            color = default_color
            label = ""
            if len(i) > 1:
                i = i[-1].split("-")
                color = i[0]

                if len(i) > 1:
                    label = i[-1]
            res.append(Stroke(sites[0], sites[-1], color, label, "@".join(i)))
        return res


if __name__ == "__main__":
    pass
