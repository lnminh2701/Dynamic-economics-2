%% File Info.

%{

    simulate.m
    ----------
    This code simulates the model.

%}

%% Simulate class.

classdef simulate
    methods(Static)
        %% Simulate the model. 
        
        function sim = lc(par,sol)            
            %% Set up.
            
            agrid = par.agrid;
            apol = sol.a;
            cpol = sol.c;
            

            TT = par.TT;
            NN = par.NN;
            T = par.T;
            tr = par.tr;
            Gt = par.Gt;

            kappa = par.kappa;
            ygrid = par.ygrid;
            pmat = par.pmat;

            ysim = nan(TT,NN);
            asim = nan(TT,NN);
            tsim = nan(TT,NN);
            csim = nan(TT,NN);
            usim = nan(TT,NN);
            gtsim = nan(TT,NN); % Container for G_t values
            
            %% Begin simulation.
            
            rng(par.seed);
            pmat0 = pmat^100; % Stationary distribution
            cmat = cumsum(pmat,2); % CDF matrix

            y0_ind = randsample(par.ylen,NN,true,pmat0(1,:))';
            a0_ind = randsample(par.alen,NN,true)';
            t0_ind = ones(T,NN)'; % Initial ages
            yr = nan(NN,1); % Pension buffer

            for i = 1:NN
                if t0_ind(i) >= tr
                    yr(i) = ygrid(y0_ind(i));
                    ysim(1,i) = kappa * yr(i) * Gt(tr-1);
                else
                    ysim(1,i) = Gt(1) * ygrid(y0_ind(i));
                end

                tsim(1,i) = t0_ind(i);
                csim(1,i) = cpol(a0_ind(i), t0_ind(i), y0_ind(i));
                asim(1,i) = apol(a0_ind(i), t0_ind(i), y0_ind(i));

                if t0_ind(i) == tr - 1
                    yr(i) = ygrid(y0_ind(i));
                elseif t0_ind(i) < tr - 1
                    y1_ind = find(rand <= cmat(y0_ind(i),:));
                    y0_ind(i) = y1_ind(1);
                end
            end

            usim(1,:) = model.utility(csim(1,:), par);

            %% Simulate next periods
            
            for j = 2:TT
                for i = 1:NN
                    age = tsim(j-1,i) + 1;

                    if age <= T
                        if age >= tr
                            ysim(j,i) = kappa * yr(i) * Gt(tr-1);
                        else
                            ysim(j,i) = Gt(age)*ygrid(y0_ind(i));
                        end

                        tsim(j,i) = age;
                        at_ind = find(asim(j-1,i) == agrid);
                        csim(j,i) = cpol(at_ind, age, y0_ind(i));
                        asim(j,i) = apol(at_ind, age, y0_ind(i));
                        usim(j,i) = model.utility(csim(j,i), par);

                        if age == tr - 1
                            yr(i) = ygrid(y0_ind(i));
                        elseif age < tr - 1
                            y1_ind = find(rand <= cmat(y0_ind(i),:));
                            y0_ind(i) = y1_ind(1);
                        end
                    end
                end
            end

            %% Output structure
            sim = struct();
            sim.ysim = ysim;
            sim.asim = asim;
            sim.tsim = tsim;
            sim.csim = csim;
            sim.usim = usim;
            sim.gtsim = gtsim;
        end
    end
end
