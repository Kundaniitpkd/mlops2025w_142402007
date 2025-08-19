clear
echo "---- sum of N numbers in shell script -------"
echo -n "Enter the Number:"
read digit
t=1
total=0
while test $t -le $digit
do
total=`expr $total + $t`
t=`expr $t + 1`
done
echo "sum of $digit: $total"
#
