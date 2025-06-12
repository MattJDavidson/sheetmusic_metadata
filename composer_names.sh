#!/bin/bash
# shellcheck disable=SC2034

# This file contains a mapping of common composer last names (from filenames)
# to their full names for PDF metadata population.
# It is sourced by the main bash_metadata_script.sh.

declare -A composer_full_names

# A
composer_full_names["Adams"]="John Adams"
composer_full_names["Albeniz"]="Isaac Albéniz"
composer_full_names["Albinoni"]="Tomaso Albinoni"
composer_full_names["Alkan"]="Charles-Valentin Alkan"
composer_full_names["Arensky"]="Anton Arensky"
composer_full_names["Arriaga"]="Juan Crisóstomo Arriaga"
composer_full_names["Auerbach"]="Lera Auerbach"

# B
composer_full_names["Bach"]="Johann Sebastian Bach"
composer_full_names["CPEBach"]="Carl Philipp Emanuel Bach"
composer_full_names["JCBach"]="Johann Christian Bach"
composer_full_names["WFBach"]="Wilhelm Friedemann Bach"
composer_full_names["Balakirev"]="Mily Balakirev"
composer_full_names["Barber"]="Samuel Barber"
composer_full_names["Bartok"]="Béla Bartók"
composer_full_names["Beethoven"]="Ludwig van Beethoven"
composer_full_names["Bellini"]="Vincenzo Bellini"
composer_full_names["Berg"]="Alban Berg"
composer_full_names["Berio"]="Luciano Berio"
composer_full_names["Berlioz"]="Hector Berlioz"
composer_full_names["Bernstein"]="Leonard Bernstein"
composer_full_names["Bizet"]="Georges Bizet"
composer_full_names["Bloch"]="Ernest Bloch"
composer_full_names["Boccherini"]="Luigi Boccherini"
composer_full_names["Borodin"]="Alexander Borodin"
composer_full_names["Boulez"]="Pierre Boulez"
composer_full_names["Brahms"]="Johannes Brahms"
composer_full_names["Britten"]="Benjamin Britten"
composer_full_names["Bruch"]="Max Bruch"
composer_full_names["Bruckner"]="Anton Bruckner"
composer_full_names["Buxtehude"]="Dietrich Buxtehude"
composer_full_names["Byrd"]="William Byrd"

# C
composer_full_names["Cage"]="John Cage"
composer_full_names["Caldara"]="Antonio Caldara"
composer_full_names["Carter"]="Elliott Carter"
composer_full_names["Cesti"]="Antonio Cesti"
composer_full_names["Chabrier"]="Emmanuel Chabrier"
composer_full_names["Charpentier"]="Marc-Antoine Charpentier"
composer_full_names["Chausson"]="Ernest Chausson"
composer_full_names["Chopin"]="Frédéric Chopin"
composer_full_names["Cimarosa"]="Domenico Cimarosa"
composer_full_names["Clementi"]="Muzio Clementi"
composer_full_names["Copland"]="Aaron Copland"
composer_full_names["Corelli"]="Arcangelo Corelli"
composer_full_names["Couperin"]="François Couperin"
composer_full_names["Crumb"]="George Crumb"
composer_full_names["Cui"]="César Cui"
composer_full_names["Czerny"]="Carl Czerny"

# D
composer_full_names["Debussy"]="Claude Debussy"
composer_full_names["Delibes"]="Léo Delibes"
composer_full_names["Delius"]="Frederick Delius"
composer_full_names["Donizetti"]="Gaetano Donizetti"
composer_full_names["Dowland"]="John Dowland"
composer_full_names["Dukas"]="Paul Dukas"
composer_full_names["Dvorak"]="Antonín Dvořák"

# E
composer_full_names["Elgar"]="Edward Elgar"
composer_full_names["Enescu"]="George Enescu"

# F
composer_full_names["Falla"]="Manuel de Falla"
composer_full_names["Faure"]="Gabriel Fauré"
composer_full_names["Feldman"]="Morton Feldman"
composer_full_names["Franck"]="César Franck"
composer_full_names["Frescobaldi"]="Girolamo Frescobaldi"

# G
composer_full_names["Gabrieli"]="Giovanni Gabrieli"
composer_full_names["Gershwin"]="George Gershwin"
composer_full_names["Gesualdo"]="Carlo Gesualdo"
composer_full_names["Gibbons"]="Orlando Gibbons"
composer_full_names["Ginastera"]="Alberto Ginastera"
composer_full_names["Glass"]="Philip Glass"
composer_full_names["Glazunov"]="Alexander Glazunov"
composer_full_names["Glinka"]="Mikhail Glinka"
composer_full_names["Gluck"]="Christoph Willibald Gluck"
composer_full_names["Gounod"]="Charles Gounod"
composer_full_names["Grieg"]="Edvard Grieg"

# H
composer_full_names["Handel"]="George Frideric Handel"
composer_full_names["Haydn"]="Joseph Haydn"
composer_full_names["Henze"]="Hans Werner Henze"
composer_full_names["Hildegard"]="Hildegard von Bingen"
composer_full_names["Hindemith"]="Paul Hindemith"
composer_full_names["Holst"]="Gustav Holst"
composer_full_names["Honegger"]="Arthur Honegger"
composer_full_names["Hummel"]="Johann Nepomuk Hummel"

# I
composer_full_names["Ives"]="Charles Ives"

# J
composer_full_names["Janacek"]="Leoš Janáček"
composer_full_names["Joplin"]="Scott Joplin"
composer_full_names["Josquin"]="Josquin des Prez"

# K
composer_full_names["Khachaturian"]="Aram Khachaturian"
composer_full_names["Kodaly"]="Zoltán Kodály"
composer_full_names["Kreisler"]="Fritz Kreisler"
composer_full_names["Kreutzer"]="Rodolphe Kreutzer"

# L
composer_full_names["Lalo"]="Édouard Lalo"
composer_full_names["Lassus"]="Orlande de Lassus"
composer_full_names["Lehar"]="Franz Lehár"
composer_full_names["Ligeti"]="György Ligeti"
composer_full_names["Liszt"]="Franz Liszt"
composer_full_names["Lully"]="Jean-Baptiste Lully"
composer_full_names["Lutoslawski"]="Witold Lutosławski"

# M
composer_full_names["Machaut"]="Guillaume de Machaut"
composer_full_names["Mahler"]="Gustav Mahler"
composer_full_names["Mascagni"]="Pietro Mascagni"
composer_full_names["Massenet"]="Jules Massenet"
composer_full_names["Mendelssohn"]="Felix Mendelssohn"
composer_full_names["Messiaen"]="Olivier Messiaen"
composer_full_names["Meyerbeer"]="Giacomo Meyerbeer"
composer_full_names["Milhaud"]="Darius Milhaud"
composer_full_names["Monteverdi"]="Claudio Monteverdi"
composer_full_names["Mozart"]="Wolfgang Amadeus Mozart"
composer_full_names["Mussorgsky"]="Modest Mussorgsky"

# N
composer_full_names["Nielsen"]="Carl Nielsen"

# O
composer_full_names["Offenbach"]="Jacques Offenbach"
composer_full_names["Orff"]="Carl Orff"

# P
composer_full_names["Pachelbel"]="Johann Pachelbel"
composer_full_names["Paganini"]="Niccolò Paganini"
composer_full_names["Palestrina"]="Giovanni Pierluigi da Palestrina"
composer_full_names["Part"]="Arvo Pärt"
composer_full_names["Pergolesi"]="Giovanni Battista Pergolesi"
composer_full_names["Poulenc"]="Francis Poulenc"
composer_full_names["Prokofiev"]="Sergei Prokofiev"
composer_full_names["Puccini"]="Giacomo Puccini"
composer_full_names["Purcell"]="Henry Purcell"

# R
composer_full_names["Rachmaninoff"]="Sergei Rachmaninoff"
composer_full_names["Rameau"]="Jean-Philippe Rameau"
composer_full_names["Ravel"]="Maurice Ravel"
composer_full_names["Reger"]="Max Reger"
composer_full_names["Respighi"]="Ottorino Respighi"
composer_full_names["Rimsky-Korsakov"]="Nikolai Rimsky-Korsakov"
composer_full_names["Rossini"]="Gioachino Rossini"

# S
composer_full_names["Saint-Saens"]="Camille Saint-Saëns"
composer_full_names["Sarasate"]="Pablo de Sarasate"
composer_full_names["Satie"]="Erik Satie"
composer_full_names["ScarlattiA"]="Alessandro Scarlatti"
composer_full_names["ScarlattiD"]="Domenico Scarlatti"
composer_full_names["Schoenberg"]="Arnold Schoenberg"
composer_full_names["Schubert"]="Franz Schubert"
composer_full_names["Schumann"]="Robert Schumann"
composer_full_names["Schutz"]="Heinrich Schütz"
composer_full_names["Scriabin"]="Alexander Scriabin"
composer_full_names["Shostakovich"]="Dmitri Shostakovich"
composer_full_names["Sibelius"]="Jean Sibelius"
composer_full_names["Smetana"]="Bedřich Smetana"
composer_full_names["Sousa"]="John Philip Sousa"
composer_full_names["StraussJ"]="Johann Strauss II" # The Waltz King
composer_full_names["StraussR"]="Richard Strauss"   # The opera/tone poem composer
composer_full_names["Stravinsky"]="Igor Stravinsky"
composer_full_names["Suppe"]="Franz von Suppé"
composer_full_names["Sweelinck"]="Jan Pieterszoon Sweelinck"
composer_full_names["Szymanowski"]="Karol Szymanowski"

# T
composer_full_names["Tallis"]="Thomas Tallis"
composer_full_names["Tchaikovsky"]="Pyotr Ilyich Tchaikovsky"
composer_full_names["Telemann"]="Georg Philipp Telemann"
composer_full_names["Thomas"]="Ambroise Thomas"

# V
composer_full_names["Varese"]="Edgard Varèse"
composer_full_names["VaughanWilliams"]="Ralph Vaughan Williams"
composer_full_names["Verdi"]="Giuseppe Verdi"
composer_full_names["Victoria"]="Tomás Luis de Victoria"
composer_full_names["Villa-Lobos"]="Heitor Villa-Lobos"
composer_full_names["Vivaldi"]="Antonio Vivaldi"

# W
composer_full_names["Wagner"]="Richard Wagner"
composer_full_names["Walton"]="William Walton"
composer_full_names["Weber"]="Carl Maria von Weber"
composer_full_names["Webern"]="Anton Webern"
composer_full_names["Widor"]="Charles-Marie Widor"
composer_full_names["Wolf"]="Hugo Wolf"
