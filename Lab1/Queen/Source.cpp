#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>

#define MAX_LENGTH 20
typedef int solutionType[MAX_LENGTH];

typedef struct
{
    solutionType solution;
    float energy;
} memberType;

#define INITIAL_TEMPERATURE 30.0
#define FINAL_TEMPERATURE 0.5
#define ALPHA 0.98
#define STEPS_PER_CHANGE 100

void tweakSolution(memberType* member)
{
    int temp, x, y;
    x = rand() % MAX_LENGTH;
    do
    {
        y = rand() % MAX_LENGTH;
    } while (x == y);
    temp = member->solution[x];
    member->solution[x] = member->solution[y];
    member->solution[y] = temp;
}

void initializeSolution(memberType* member)
{
    int i;

    for (i = 0; i < MAX_LENGTH; i++)
    {
        member->solution[i] = i;
    }

    for (i = 0; i < MAX_LENGTH; i++)
    {
        tweakSolution(member);
    }
}

void computeEnergy(memberType* member)
{
    int i, j, x, y, tempx, tempy;
    char board[MAX_LENGTH][MAX_LENGTH];
    int conflicts;
    const int dx[4] = { -1, 1, -1, 1 };
    const int dy[4] = { -1, 1, 1, -1 };

    for (i = 0; i < MAX_LENGTH; i++)
    {
        for (j = 0; j < MAX_LENGTH; j++)
        {
            board[i][j] = 0;
        }
    }
    for (i = 0; i < MAX_LENGTH; i++)
    {
        board[i][member->solution[i]] = 'Q';
    }

    conflicts = 0;

    for (i = 0; i < MAX_LENGTH; i++)
    {
        x = i;
        y = member->solution[i];
        for (j = 0; j < 4; j++)
        {
            tempx = x;
            tempy = y;
            while (1)
            {
                tempx += dx[j];
                tempy += dy[j];
                if ((tempx < 0) || (tempx >= MAX_LENGTH) || (tempy < 0) || (tempy >= MAX_LENGTH))
                {
                    break;
                }
                if (board[tempx][tempy] == 'Q')
                {
                    conflicts++;
                }
            }
        }
    }
    member->energy = (float)conflicts;
}

void copySolution(memberType* dest, memberType* src)
{
    int i;

    for (i = 0; i < MAX_LENGTH; i++)
    {
        dest->solution[i] = src->solution[i];
    }
    dest->energy = src->energy;
}

void emitSolution(memberType* member)
{
    char board[MAX_LENGTH][MAX_LENGTH];
    int x, y;

    for (int i = 0; i < MAX_LENGTH; i++)
    {
        for (int j = 0; j < MAX_LENGTH; j++)
        {
            board[i][j] = 0;
        }
    }

    for (x = 0; x < MAX_LENGTH; x++)
    {
        board[x][member->solution[x]] = 'Q';
    }

    printf("board:\n");
    for (y = 0; y < MAX_LENGTH; y++)
    {
        for (x = 0; x < MAX_LENGTH; x++)
        {
            if (board[x][y] == 'Q')
            {
                printf("Q ");
            }
            else
            {
                printf("- ");
            }
        }
        printf("\n");
    }
    printf("\n");
}

int main()
{
    int step, solution = 0, useNew, accepted;
    float temperature = INITIAL_TEMPERATURE;
    char board[MAX_LENGTH][MAX_LENGTH];
    int x, y;
    memberType current, working, best;

    srand(time(NULL));

    initializeSolution(&current);
    emitSolution(&current);
    computeEnergy(&current);
    best.energy = 100.0;
    copySolution(&working, &current);

    while (temperature > FINAL_TEMPERATURE)
    {
        accepted = 0;

        for (step = 0; step < STEPS_PER_CHANGE; step++)
        {
            useNew = 0;

            tweakSolution(&working);
            computeEnergy(&working);

            if (working.energy <= current.energy)
            {
                useNew = 1;
            }
            else
            {
                float test = rand();
                float delta = working.energy - current.energy;
                float calc = exp(-delta / temperature);

                if (calc > test)
                {
                    accepted++;
                    useNew = 1;
                }
            }

            if (useNew)
            {
                useNew = 0;
                copySolution(&current, &working);

                if (current.energy < best.energy)
                {
                    copySolution(&best, &current);
                    solution = 1;
                }
            }
            else
            {
                copySolution(&working, &current);
            }
        }
        temperature *= ALPHA;
    }

    if (solution)
    {
        emitSolution(&best);
    }
    return 0;
}