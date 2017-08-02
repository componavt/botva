#!/usr/bin/env python
# -*- coding: utf-8 -*-

print 'Start computation.'

variety = ["А. Д. Александров", "О. М. Белоцерковский", "С. Н. Бернштейн"]
expert  = ["А. Д. Александров", "С. Н. Бернштейн", "О. М. Белоцерковский"]

print "\nRating by variety:"
print ', '.join(variety)

print "\nRating by expert:"
print ', '.join(expert)

print "\n"

# get all pairs from first list: variety
rating_distance = 0
for i in range(0, len(variety)):
    for j in range(i+1, len(variety)):
        print "Vareity pair(%s, %s)." % (variety[i], variety[j])
        first_in_expert  = expert.index( variety[i] )
        second_in_expert = expert.index( variety[j] )
        print "Expert index(%d, %d)." % (first_in_expert, second_in_expert)


print "\nDistance between variety rating and expert rating is %d." % rating_distance
