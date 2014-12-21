#! /bin/sh
rootDir=$HOME/.question
umask 022
if [ ! -d "$rootDir" ] ; then 	
	mkdir "$rootDir" && mkdir "${rootDir}/answers" && mkdir "${rootDir}/questions" && mkdir "${rootDir}/votes" && mkdir "${rootDir}/usr"|| { echo "Create File Error" 1>&2 ; exit 1 ; } 
fi
# echo "$1"
case "$1" in 
	[Cc]reate) if [ $# -gt 3 ] ; then 
					echo "Arguments too many! Usage: $0 $1 name [question]" 1>&2
					exit 1
				 elif [ $# -le 1 ] ; then
					echo "Arguments too few! Usage: $0 $1 name [question]" 1>&2
					exit 1
			     else
			     	#find "$rootDir/questions" -type f | grep ".*/$2$" >&2
			     	[ -f "$rootDir/questions/$2" ]
			     	if [ $? -eq 0 ] ; then 
			     		echo "You have asked the question $2 before." 1>&2
						exit 2						     
					else	 
						echo $2 | grep ".*/.*" >&2 
						if [ $? -eq 0 ]; then # name contains a front slash
							echo "Invalid: Name contains front slash" >&2 
							exit 2
                        else 
                        	if [ $# -eq 2 ]; then
								read questionContent
							else 
								questionContent="$3"
							fi
							case "$questionContent" in 
								"" ) echo "The question is empty!" 1>&2 ; exit 2 ;;
								*====*) echo "Your question contains invalid character sequence!" 1>&2 ; exit 2 ;; 
								*[![:space:]]*) 
									echo "$questionContent" > "$rootDir/questions/$2" 
								    if [ $? -eq 0 ] ; then 
									   	exit 
								 	else 
								   		echo "Creating the question error" >&2 
								    	exit 2 
									fi 
									;;								 
								*) echo "Your question contains only space or tab" >&2; exit 2 ;;
							esac
						fi
					fi
				fi
				;;
	[Aa]nswer) if [ $# -gt 4 ] ; then 
					echo "Arguments too many! Usage: $0 $1 question_id name [answer]" 1>&2
					exit 1
				 elif [ $# -le 2 ] ; then
					echo "Arguments too few! Usage: $0 $1 question_id name [answer]" 1>&2
					exit 1
			     else
			     	echo $3 | grep ".*/.*" >&2 
			     	if [ $? -eq 0 ]; then # name contains a front slash
							echo "Invalid: Name contains front slash" >&2 
							exit 2
					else
						questionUser=`echo "$2" | sed -n "s/\(.*\)\/\(.*\)/\1/p"`
						questionName=`echo "$2" | sed -n "s/\(.*\)\/\(.*\)/\2/p"`
						# check whether do we have the question or not
						#find "/home/$questionUser/.question/questions" -type f | grep ".*/$questionName$" 2>&1 1>/dev/null 
						[ -f "/home/$questionUser/.question/questions/$questionName" ] 
						# grep failed; no such question
						if [ $? -ne 0 ] ; then      
							echo "No such Question $2" >&2
							exit 2
						fi
						if [ ! -d "$rootDir/answers/$questionUser" ] ; then    # the directory of user not exist
							mkdir "$rootDir/answers/$questionUser"
							if [ $? -ne 0 ]; then
								echo "Create $questionUser in your local directory error" >&2
								exit 2
							fi
						fi
						if [ ! -d "$rootDir/answers/$questionUser/$questionName" ] ; then  # the directory for the question not exist
							mkdir "$rootDir/answers/$questionUser/$questionName"
							if [ ! $? -eq 0 ]; then
								echo "Create Directory $questionName error" >&2
								exit 2
							fi
						fi
						if [ -f "$rootDir/answers/$questionUser/$questionName/$3" ] ; then
								echo "You has already answered the question $2 with answer $3" >&2
								exit 2
							else # now we have the directory and need to take care of the content
								if [ $# -eq 3 ] ; then
									read answerContent
								else 
									answerContent="$4"
								fi
								case "$answerContent" in 
									"") echo "The answer is empty!" 1>&2 ; exit 2 ;;
									*====*) echo "Your answer contains invalid character sequence!" 1>&2 ; exit 2 ;; 
									*[![:space:]]*) echo "$answerContent" > "$rootDir/answers/$questionUser/$questionName/$3" ;
										if [ $? -eq 0 ] ; then
											exit 
										else
										 	echo "Creating the answer error" >&2 
									 		exit 2 
										fi
										;;
									*) echo "Your answer contains only space or tab" >&2; exit 2 ;;
								esac
						fi
					fi
				fi
				;;
	[Ll]ist )	if [ $# -gt 2 ]; then
					echo "Two many arguments! Usage: $0 $1 [user]" >&2 
					exit 2
				elif [ $# -eq 0 ] ; then 
					echo "Two few arguments! Usage: $0 $1 [user]" >&2
					exit 2
				elif [ $# -eq 1 ]; then  # list all users
					for var in `cat /home/unixtool/data/question/users` ; do
						find "/home/$var/.question/questions/" -type f 2>/dev/null | sed -n "s/.*\/\(.*\)$/$var\/\1/p"
					done
					exit
				else
					find "/home/$2/.question/questions" -type f 2>/dev/null | sed -n "s/.*\/\(.*\)$/$2\/\1/p"   #| sed -n "/^\.\/$2\/[^/]*$/s/\.\/\(.*\)\/\(.*\)$/\1\/\2/p"
					exit
				fi
	;;
	[Vv]ote ) if [ $# -gt 4 ]; then
					echo "Two many arguments! Usage: $0 $1 up|down question_id [answer_id]" >&2 
					exit 2
			  	elif [ $# -lt 3 ]; then
			  		echo "Two few arguments! Usage: $0 $1 up|down question_id [answer_id]" >&2
					exit 2
			 	elif [ $# -eq 3 ]; then    #vote the question
			  		questionUser=`echo "$3" | sed -n "s/\(.*\)\/\(.*\)/\1/p"`
					questionName=`echo "$3" | sed -n "s/\(.*\)\/\(.*\)/\2/p"`
						# check whether do we have the question or not
					#find "/home/$questionUser/.question/questions" -type f | grep ".*/$questionName$" 2>&1 1>/dev/null 
					[ -f "/home/$questionUser/.question/questions/$questionName" ]
						# grep failed; no such question
					if [ $? -ne 0 ] ; then      
						echo "No such Question $3" >&2
						exit 2
					fi
					if [ ! -d "$rootDir/votes/$questionUser" ] ; then    # the directory of user not exist
						mkdir "$rootDir/votes/$questionUser"
						if [ $? -ne 0 ]; then
							echo "Create $questionUser in your local directory error" >&2
							exit 2
						fi
					fi
					echo "$2" | grep -v -E 'up|down' >&2
					if [ $? -eq 0 ]; then   # not match up or down
						echo "Invalid $2" >&2
						exit 2
					fi
					echo "$2" >> "$rootDir/votes/$questionUser/$questionName"
					exit
			  	else   # vote for the answer
			  		questionUser=`echo "$3" | sed -n "s/\(.*\)\/\(.*\)/\1/p"`
			  		questionName=`echo "$3" | sed -n "s/\(.*\)\/\(.*\)/\2/p"`
			  		answerUser=`echo "$4" | sed -n "s/\(.*\)\/\(.*\)/\1/p"`
			  		answerName=`echo "$4" | sed -n "s/\(.*\)\/\(.*\)/\2/p"`
			  		#find "/home/$questionUser/.question/questions" -type f | grep ".*/$questionName$" 2>&1 1>/dev/null 
			  		[ -f "/home/$questionUser/.question/questions/$questionName" ]
						# grep failed; no such question
					if [ $? -ne 0 ] ; then      
						echo "No such Question $3" >&2
						exit 2
					fi
					# check whether the answer exist
					#find "/home/$answerUser/.question/answers/$questionUser/$questionName" -type f 2>/dev/null | grep ".*/$answerName$" >/dev/null
					[ -f "/home/$answerUser/.question/answers/$questionUser/$questionName/$answerName" ] 
					if [ $? -ne 0 ]; then   #grep failed; no such answer
						echo "No such answer $4" >&2
						exit 2
					fi
					if [ ! -d "$rootDir/votes/$questionUser" ] ; then    # the directory of user not exist
						mkdir "$rootDir/votes/$questionUser"
						if [ $? -ne 0 ]; then
							echo "Create $questionUser in your local directory error" >&2
							exit 2
						fi
					fi
					echo "$2" | grep -v -E 'up|down' >&2
					if [ $? -eq 0 ]; then   # not match up or down
						echo "Invalid $2" >&2
						exit 2
					fi
					echo "$2 $4" >> "$rootDir/votes/$questionUser/$questionName"
					exit
				fi
				;;
	[Vv]iew ) if [ $# -le 1 ]; then
			 	echo "Two few arguments. Usage: $0 $1 question_id ..." >&2
			 	exit 2
			  fi
			  shift
			  for var in "$@" ; do
			  	questionUser=`echo "$var" | sed -n "s/\(.*\)\/\(.*\)/\1/p"`
			  	questionName=`echo "$var" | sed -n "s/\(.*\)\/\(.*\)/\2/p"`
			  	#find "/home/$questionUser/.question/questions" -type f | grep ".*/$questionName$" 2>&1 1>/dev/null 
			  	[ -f "/home/$questionUser/.question/questions/$questionName" ]
						# grep failed; no such question
				if [ $? -ne 0 ] ; then      
					echo "No such Question $var" >&2
					exit 2
				fi
				# get votes from all users
				declare -A resultArray
				resultArray[$questionName]=0
				# $var here is the question_id; to distingush from the answer_id only store the question name here
				for user in `cat /home/unixtool/data/question/users` ; do
					#first add all the answer_id
					anFileName=`find "/home/$user/.question/answers/$questionUser/$questionName/" -type f 2>/dev/null` 
					#echo $anFileName
					if [ -n "$anFileName" ] ; then
						while read q ; do
							ansName=`echo $q | sed -n "s/.*\/\(.*\)$/\1/p"`
							resultArray["${user}/${ansName}"]=0
							#echo "resultArray length ${#resultArray[*]}"
							#echo "${user}/${ansName}"
						done <<<"$anFileName"
					fi
					#update votes
					fileName=`find "/home/$user/.question/votes/$questionUser/$questionName" 2>/dev/null` 
					if [ -z "$fileName" ]; then
						continue
					fi
					
					declare -A localArray
					#echo "localArray length ${#localArray[*]}"
					while read p ; do							
						set $p
						if [ $# -eq 1 ]; then  # vote the question
							localArray["$questionName"]=$1
						else
							answer_id=`echo $p | sed -n "s/^[^[:space:]]* \(.*\)$/\1/p"`
							localArray["$answer_id"]=$1
						fi
					done < "$fileName"
					for arrIndex in "${!localArray[@]}"; do
						if [ ${localArray[$arrIndex]} = "up" ]; then
							#echo "plus"
							resultArray[$arrIndex]=`expr ${resultArray[$arrIndex]} + 1` #$((${resultArray[$arrIndex]} + 1))  
						else
							#echo "minus"
							resultArray[$arrIndex]=`expr ${resultArray[$arrIndex]} - 1` #$((${resultArray[$arrIndex]} - 1))  # 	
						fi
					done	
					unset localArray
				done	
				#loop through all the user; should print the whole result
				#echo "resultArray length ${#resultArray[*]}"
				echo "${resultArray[$questionName]}"
				cat "/home/$questionUser/.question/questions/$questionName"
				echo "===="
				for index in "${!resultArray[@]}"; do
					
					echo $index | grep "^.*/.*$" 2>&1 1>/dev/null
					# not match --> it's the question			
					if [ $? -ne 0 ]; then		
						continue
					else
						echo "${resultArray[$index]}" 
						answerUser=`echo "$index" | sed -n "s/\(.*\)\/\(.*\)/\1/p"`
			  			answerName=`echo "$index" | sed -n "s/\(.*\)\/\(.*\)/\2/p"`
			  			echo "Answer Path: /home/$answerUser/.question/answers/$questionUser/$questionName/$answerName"
			  			#echo "$index"
			  			cat "/home/$answerUser/.question/answers/$questionUser/$questionName/$answerName"
			  			echo "===="
					fi
				done
				unset resultArray	
			done
			exit
		;;	
	*) echo "No such option exist" >&2 ; exit 1 ;;
esac
