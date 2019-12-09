def fuel(x)
    (x/3).floor - 2
end

def fuel2(x)
    f = fuel(x)
    if f <= 0
        return 0
    end
    [f + fuel2(f), 0].max
end

lines = File.readlines "day01_input.txt"
lines = lines.map(&:strip).map(&:to_i)
puts 'part 1', lines.map{ |x| fuel(x) }.sum
puts 'part 2', lines.map{ |x| fuel2(x) }.sum
