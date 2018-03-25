for file in `cat ias_jul_url.txt`
    do
        echo "Started" $file
        python3 ias_url.py $file >>ias_art_url.txt
        echo "Finished" $file

    done
