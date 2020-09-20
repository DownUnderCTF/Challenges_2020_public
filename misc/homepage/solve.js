// Just paste this script onto the homepage
// Courtesy of Joseph (MISC)

const mouseover = new Event('mouseover')

// activate all the dots
document.querySelectorAll("#logo circle").forEach((c) => c.dispatchEvent(mouseover))

// getting all the dots
var dots = Array(...document.querySelectorAll('#logo circle'))

// sort dots by y pos, then x pos
function sort_lr_tb(a, b) {
    ax = a.cx.baseVal.value
    bx = b.cx.baseVal.value
    ay = a.cy.baseVal.value
    by = b.cy.baseVal.value
    if(ax == bx) return ay - by
    return ax - bx
}

var sorted_dots = dots.sort(sort_lr_tb)

var zero_fill = sorted_dots[0].style.fill

// get binary
var out = sorted_dots.map(x => x.style.fill == zero_fill ? '0' : '1').join('')

// decode ascii
var decoded = ''
for(var i = 0; i < out.length; i += 8) {
    var c = parseInt(out.substr(i, 8), 2)
    decoded += String.fromCharCode(c)
}

console.log(decoded)
