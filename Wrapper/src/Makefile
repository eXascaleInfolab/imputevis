all:
	g++ -O3 -D ARMA_DONT_USE_WRAPPER -fPIC -rdynamic -shared -o libAlgoCollection.so -Wall -Werror -Wextra -pedantic -Wconversion -Wsign-conversion -msse2 -msse3 -msse4 -msse4.1 -msse4.2 -fopenmp -std=gnu++14 Algebra/Auxiliary.cpp Algorithms/TKCM.cpp Algorithms/ST_MVL.cpp Algorithms/SPIRIT.cpp Algorithms/GROUSE.cpp Algorithms/NMFMissingValueRecovery.cpp Algorithms/DynaMMo.cpp Algorithms/SVT.cpp Algorithms/ROSL.cpp Algorithms/IterativeSVD.cpp Algorithms/SoftImpute.cpp Algorithms/CDMissingValueRecovery.cpp Algebra/CentroidDecomposition.cpp Algebra/RSVD.cpp Stats/Correlation.cpp shared/SharedLibFunctions.cpp -lopenblas -larpack -lmlpack

nomlpack:
	g++ -O3 -D ARMA_DONT_USE_WRAPPER -fPIC -rdynamic -shared -o libAlgoCollection.so -Wall -Werror -Wextra -pedantic -Wconversion -Wsign-conversion -msse2 -msse3 -msse4 -msse4.1 -msse4.2 -fopenmp -std=gnu++14 Algebra/Auxiliary.cpp Algorithms/TKCM.cpp Algorithms/ST_MVL.cpp Algorithms/SPIRIT.cpp Algorithms/GROUSE.cpp Algorithms/DynaMMo.cpp Algorithms/SVT.cpp Algorithms/ROSL.cpp Algorithms/IterativeSVD.cpp Algorithms/SoftImpute.cpp Algorithms/CDMissingValueRecovery.cpp Algebra/CentroidDecomposition.cpp Algebra/RSVD.cpp Stats/Correlation.cpp shared/SharedLibFunctions.cpp -lopenblas -larpack

brian:
	g++ -O3 -D ARMA_DONT_USE_WRAPPER -fPIC -rdynamic -shared -o libAlgoCollection.so -Wall -Werror -Wextra -pedantic -Wconversion -Wsign-conversion -msse2 -msse3 -msse4 -msse4.1 -msse4.2 -fopenmp -std=gnu++14 Algebra/Auxiliary.cpp Algorithms/ST_MVL.cpp Algorithms/CDMissingValueRecovery.cpp Algebra/CentroidDecomposition.cpp Algebra/RSVD.cpp Stats/Correlation.cpp shared/SharedLibFunctions.cpp -lopenblas -larpack

clean:
	rm libAlgoCollection.so
