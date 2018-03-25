for file in `cat springer/springer_jur_url.txt`
    do
        echo "Started" $file
        python3 springer/springer_url.py $file >> springer/springer_all_volume.txt
        echo "Finished" $file

    done
