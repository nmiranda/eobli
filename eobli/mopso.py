#!/usr/bin/env python

import numpy as np
import pylab as pl
import random
from modelojorgereyes import modelo
from joblib import Parallel, delayed

np.random.seed(42)

pop_size = 40
repo_size = 200
grid_partitions = 10
iterations = 500
in_dimensions = 2
out_dimensions = 2
upper_bounds = np.array([1.312, 40])
lower_bounds = np.array([1.001, 1.05])


def f(x):
	return np.array([
		x[0],
		(1 + 10 * x[1]) * (1 - (x[0] / (1 + 10 * x[1])) ** 2 - (x[0] * np.sin(2 * np.pi * 4 * x[0]) / (1 + 10 * x[1])))
	])

def g(x):
	I = 3
	S = x[0]
	Flow = x[1]
	n_fluido = 45
	col_celda = 4
	col_fluido = 5
	return np.array(
		modelo(I, S, Flow, n_fluido, col_celda, col_fluido)
	)

def dominance(x, y):
	# 1 : x dominates y (x has smaller components than y)
	# -1: y dominates x (x has smaller components than x)
	# 0: none of the above
	dimensions = len(x)
	matches_table = [0] * dimensions
	for i in range(dimensions):
		if x[i] < y[i]:
			matches_table[i] = 1
		if x[i] > y[i]:
			matches_table[i] = -1
	if -1 in matches_table and 1 in matches_table:
		return 0;
	elif 1 in matches_table:
		return 1
	elif -1 in matches_table:
		return -1
	else:
		return 0

def get_bin_coordinates(individual, upper_bounds, lower_bounds, grid_partitions):
	result = np.zeros(individual.size)
	for i in range(individual.size):
		result[i] = np.floor((individual[i] - lower_bounds[i]) / (upper_bounds[i] - lower_bounds[i]) * grid_partitions)
	return result

def get_champions(population, objectives):
	champions = []
	champions_objectives = []
	for i in range(len(population)):
		champion = True
		for j in range(len(population)):
			champion = champion and (dominance(objectives[i], objectives[j]) in [0, 1])
		if champion:
			champions.append(population[i])
			champions_objectives.append(objectives[i])
	return champions, champions_objectives

def mopso(f, in_dimensions, pop_size, repo_size,  grid_partitions=10, w=0.4):

	population = np.array([[np.random.random() * (upper_bound - lower_bound) + lower_bound for (upper_bound, lower_bound) in zip(upper_bounds, lower_bounds)] for _ in range(pop_size)])
	population_velocity = np.zeros((pop_size, in_dimensions))

	objectives = np.apply_along_axis(g, 1, population)

	repository, repository_objectives = get_champions(population, objectives)

	best_historical_individuals = np.copy(population)
	best_historical_objectives = np.copy(objectives)

	w = 0.4

	bins = np.array([np.linspace(lower_bounds[i], upper_bounds[i], num=grid_partitions + 1) for i in range(in_dimensions)])

	for _ in range(iterations):
		print "Iteration %d" % _

		coarse_map = np.histogramdd(population, bins=bins)[0]

		population_loneliness = 1.0 / np.array([coarse_map[tuple(np.array([min(max(np.digitize(np.array([coordinate]), bin)[0], 0), grid_partitions) for coordinate, bin in zip(population[i], bins)]) - 1)] for i in range(len(population))])


		bests = np.random.choice(pop_size, pop_size, p=population_loneliness/np.sum(population_loneliness))
		population_velocity = w * population_velocity + np.random.random(pop_size)[:, np.newaxis] * (best_historical_individuals - population) + np.random.random(pop_size)[:, np.newaxis] * (population[bests] - population)

		population = np.clip(population + population_velocity, lower_bounds, upper_bounds)
		objectives = np.apply_along_axis(g, 1, population)

		champions, champions_objectives = get_champions(population, objectives)

		repository, repository_objectives = get_champions(repository + champions, repository_objectives + champions_objectives)

		if len(repository) > repo_size:
			coarse_map = np.histogramdd(population, bins=bins)[0]
			population_loneliness = 1.0 / np.array([coarse_map[tuple(np.array([min(max(np.digitize(np.array([coordinate]), bin)[0], 0), grid_partitions) for coordinate, bin in zip(population[i], bins)]) - 1)] for i in range(len(population))])
			surviving_indices = np.argsort(population_loneliness)[:repo_size]
			repository = [repository[i] for i in surviving_indices]
			repository_objectives = [repository_objectives[i] for i in surviving_indices]

		for i in range(len(population)):
			dominance_ = dominance(objectives[i], best_historical_objectives[i])
			if dominance_ == 1 or (dominance_ == 0 and np.random.random() > 0.5):
				best_historical_individuals[i] = population[i]
				best_historical_objectives[i] = objectives[i]

	
	# pl.clf()
	# pl.plot(np.array(repository_objectives)[:, 0], np.array(repository_objectives)[:, 1], "o")
	# pl.pause(0.001)

	return (np.array(repository), np.array(repository_objectives))

pl.close("all")

repository, repository_objectives = mopso(f, in_dimensions, pop_size, repo_size,  grid_partitions=10, w=0.4)
pl.plot(repository_objectives[:, 0], np.array(repository_objectives)[:, 1], "o")
pl.show()
