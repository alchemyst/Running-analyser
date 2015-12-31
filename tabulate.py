#!/usr/bin/env python

# generalised tabular output


def printtable(headers, data, formats=None, rowformatter=None):
    assert formats is None or rowformatter is None,\
           "formats or rowformatter must be given"
    
    # For now, assume headers
    collengths = map(len, headers)
    # for now, assume all rows have same # of cols
    alldata = list(data)
    outputrows = []
    for row in alldata:
        # Do the transforms on this row
        if formats:
            transformedrow = [f(i) for f, i in zip(formats, row)]
        elif rowformatter:
            transformedrow = rowformatter(row)
        # figure out how long each of the strings are
        lengths = map(len, transformedrow)
        collengths = map(max, zip(collengths, lengths))
        outputrows.append(transformedrow)
    outputformats = ["%%%is" % i for i in collengths]

    def rowstring(items):
        return " ".join(f % i for f, i in zip(outputformats, items))

    print rowstring(headers)
    print '-'*(sum(collengths) + len(collengths))
    for row in outputrows:
        print rowstring(row)

def doubleformatter(x):
    return "%5.3f (double)" % x

if __name__ == "__main__":
    printtable(headers=['this', 'is', 'a'],
               data=[[1.2, 'of', 'the'],
                     [4e-6, 50, 'Formatter']],
               formats=[doubleformatter, str, str])
        
