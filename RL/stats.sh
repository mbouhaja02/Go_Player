#!/bin/bash

# Initialiser les compteurs pour chaque résultat possible
black_wins=0
white_wins=0
draws=0

# Boucle pour exécuter le jeu 100 fois
for i in {1..10}
do
    result=$(python3 namedGame.py myPlayer randomPlayer)
    # echo "Game $i: $result"
    
    # Incrémenter le compteur en fonction du résultat
    if [ "$result" == "BLACK" ]; then
        ((black_wins++))
    elif [ "$result" == "WHITE" ]; then
        ((white_wins++))
    elif [ "$result" == "DEUCE" ]; then
        ((draws++))
    fi
done

# Calculer les probabilités
total_games=$((black_wins + white_wins + draws))
black_win_rate=$(echo "scale=2; $black_wins / $total_games * 1000")
white_win_rate=$(echo "scale=2; $white_wins / $total_games * 1000")
draw_rate=$(echo "scale=2; $draws / $total_games * 1000")

# Afficher les résultats
echo "Results after $total_games games:"
echo "Black wins: $black_wins ($black_win_rate%)"
echo "White wins: $white_wins ($white_win_rate%)"
echo "Draws: $draws ($draw_rate%)"
