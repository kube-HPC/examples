for i in {0..100}; do echo $i>Vehicles_$i.txt; done
for i in {0..20}; do echo "car">>Vehicles_$i.txt.meta; done
for i in {21..40}; do echo "bike">>Vehicles_$i.txt.meta; done
for i in {41..60}; do echo "truck">>Vehicles_$i.txt.meta; done
for i in {61..80}; do echo "motorcycle">>Vehicles_$i.txt.meta; done
